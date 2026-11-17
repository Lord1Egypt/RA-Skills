"""Signed, fixed-membership voting. This is a quorum evaluator, not a distributed BFT network."""
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import math
from uuid import uuid4
from .types import COEEvent, Primitive, ConsensusPolicy, VerificationResult, SharedWorldState, ConsensusResult
from .security import canonical, plain, verify_event

def event_digest(event):
    body=plain(event);body.pop('signature',None);body.pop('hash',None)
    return 'sha256:'+hashlib.sha256(canonical(body)).hexdigest()

class ConsensusEngine:
    def __init__(self,policy=ConsensusPolicy.SIMPLE_MAJORITY,*,validators=None,trusted_keys=None,session_id='local',tenant='local'):
        self.policy=ConsensusPolicy(policy)
        self.validators=frozenset(validators or [])
        self.keys=trusted_keys
        self.context={'purpose':'consensus','tenant':tenant,'session':session_id}
        self.events=[]
        self.trust_weights={v:1.0 for v in self.validators}
        self.bft_fault_tolerance=1
        self.weighted_threshold=None
        self.min_verifications=3

    def _configurable(self):
        if self.events: raise ValueError('Policy cannot change after voting starts')

    def set_trust_weight(self,issuer,weight):
        self._configurable()
        if issuer not in self.validators or not math.isfinite(weight) or not 0<=weight<=1: raise ValueError('Invalid validator weight')
        self.trust_weights[issuer]=weight

    def set_bft_params(self,fault_tolerance):
        self._configurable()
        if type(fault_tolerance) is not int or fault_tolerance<1: raise ValueError('f must be a positive integer')
        self.bft_fault_tolerance=fault_tolerance

    def set_weighted_threshold(self,threshold):
        self._configurable()
        if not math.isfinite(threshold) or threshold<=0: raise ValueError('Invalid threshold')
        self.weighted_threshold=threshold

    def add_event(self,event):
        if len(self.events)>=128: raise OverflowError('Event limit exceeded')
        if not event.event_id or any(e.event_id==event.event_id for e in self.events): raise ValueError('Duplicate or missing event ID')
        if event.timestamp.tzinfo is None or abs((datetime.now(timezone.utc)-event.timestamp).total_seconds())>300: raise ValueError('Timestamp outside acceptance window')
        if event.confidence is not None and (not math.isfinite(event.confidence) or not 0<=event.confidence<=1): raise ValueError('Invalid confidence')
        if event.hash is not None and event.hash!=event_digest(event): raise ValueError('Event digest mismatch')
        if not verify_event(event,self.context,self.keys): raise ValueError('Untrusted or invalid signature')
        if event.primitive==Primitive.JUDGE:
            if not event.assertion or set(event.assertion)!={'subject','predicate','value'}: raise ValueError('Assertion requires subject, predicate, value')
            if any(not isinstance(event.assertion[k],str) or not event.assertion[k] for k in ['subject','predicate']): raise ValueError('Invalid assertion key')
            canonical(event.assertion)
        elif event.primitive in (Primitive.VERIFY,Primitive.TERMINATE):
            refs=event.verify_of if event.primitive==Primitive.VERIFY else [event.terminate_of]
            if not refs or len(refs)!=1: raise ValueError('Exactly one judgment reference is required')
            parent=next((e for e in self.events if e.event_id==refs[0]),None)
            if not parent or parent.primitive!=Primitive.JUDGE or parent.target!=event.target or parent.timestamp>event.timestamp: raise ValueError('Invalid prior judgment reference')
            if event.reference_digest!=event_digest(parent): raise ValueError('Referenced judgment digest mismatch')
            if event.primitive==Primitive.TERMINATE and parent.issuer!=event.issuer: raise ValueError('Only the judgment issuer may terminate it')
            if event.primitive==Primitive.VERIFY and (event.issuer not in self.validators or event.issuer==parent.issuer): raise ValueError('Independent configured validator required')
        else: raise ValueError('Delegation is not a voting operation')
        self.events.append(deepcopy(event))

    def run(self,target=None):
        n=len(self.validators)
        if n<3: raise ValueError('Configure at least three distinct validators')
        if self.policy==ConsensusPolicy.BFT and n<3*self.bft_fault_tolerance+1: raise ValueError('BFT requires n >= 3f+1')
        total_weight=sum(self.trust_weights.values())
        threshold=self.weighted_threshold if self.weighted_threshold is not None else total_weight/2
        if self.policy==ConsensusPolicy.WEIGHTED_TRUST and (total_weight<=0 or threshold<total_weight/2 or threshold>=total_weight): raise ValueError('Weighted threshold must be at least half of total configured weight and below total')
        events=[e for e in self.events if target is None or e.target==target]
        if any(not verify_event(e,self.context,self.keys) for e in events): raise ValueError('Event changed after admission')
        terminated={e.terminate_of for e in events if e.primitive==Primitive.TERMINATE}
        groups=defaultdict(list)
        for e in events:
            if e.primitive==Primitive.JUDGE and e.event_id not in terminated:
                groups[(e.target,e.assertion['subject'],e.assertion['predicate'])].append(e)
        assertions=[]; conflicts=[]
        for (world,subject,predicate),judgments in groups.items():
            by_id={j.event_id:j for j in judgments}
            by_issuer=defaultdict(set); votes={}
            for v in events:
                if v.primitive!=Primitive.VERIFY or v.verify_of[0] not in by_id: continue
                value=by_id[v.verify_of[0]].assertion['value']
                key=canonical(value).decode()
                # Rejections and conflicting statements disqualify a signer for this assertion.
                vote=(key,v.verification_result.value if v.verification_result else None,v.confidence if v.confidence is not None else 1.0)
                by_issuer[v.issuer].add(vote)
            counts=defaultdict(list)
            for issuer,statements in by_issuer.items():
                if len(statements)!=1: continue
                key,result,confidence=next(iter(statements))
                if result=='confirmed' and confidence>0: counts[key].append((issuer,confidence))
            eligible=[]
            for key,ballots in counts.items():
                count=len(ballots)
                score=sum(self.trust_weights[i]*c for i,c in ballots)
                ok=count>=max(3,n//2+1)
                if self.policy==ConsensusPolicy.BFT: ok=count>=n-self.bft_fault_tolerance
                if self.policy==ConsensusPolicy.WEIGHTED_TRUST: ok=count>=3 and score>threshold
                if ok: eligible.append((key,ballots))
            if len(eligible)==1:
                import json
                key,ballots=eligible[0]
                assertions.append({'target':world,'subject':subject,'predicate':predicate,'value':json.loads(key),'confirmations':len(ballots),'confidence':len(ballots)/n,'based_on':[j.event_id for j in judgments],'consensus_policy':self.policy.value})
            else: conflicts.append({'target':world,'subject':subject,'predicate':predicate,'reason':'Configured quorum was not reached','distinct_verifiers':len(by_issuer)})
        sws=None
        if assertions:
            sws=SharedWorldState(str(uuid4()),target or 'global',datetime.now(timezone.utc),assertions)
            body=plain(sws);body.pop('hash')
            sws.hash='sha256:'+hashlib.sha256(canonical(body)).hexdigest()
        return ConsensusResult(sws,bool(assertions) and not conflicts,conflicts,self.policy,'Quorum evaluation complete. Output hash is a checksum, not an authenticated signature.',len(events),dict(Counter(e.issuer for e in events)))
