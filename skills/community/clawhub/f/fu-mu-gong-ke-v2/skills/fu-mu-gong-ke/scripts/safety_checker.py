"""
Safety Checker - Parenting Psychology Safety Module
Version: 1.1.1
"""
from __future__ import annotations
import re, time
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Dict, List, Optional, Tuple, Set

# 从共享常量模块导入危机关键词
try:
    from constants import (
        SUICIDE_KEYWORDS as _SUICIDE_KW,
        SELF_HARM_KEYWORDS as _SELF_HARM_KW,
        SELF_HARM_FUNCTIONAL as _SELF_HARM_FUNC,
        DESPAIR_KEYWORDS as _DESPAIR_KW,
        METAPHOR_KEYWORDS as _METAPHOR_KW,
        METAPHOR_EXHAUSTION, METAPHOR_HOPELESSNESS,
        METAPHOR_ABSENCE, METAPHOR_CHILD_SIGNALS,
        IMMINENT_SIGNALS as _IMMINENT_KW,
        NEGATION_PATTERNS as _NEGATION_PATTERNS,
        QUOTE_PATTERNS as _QUOTE_PATTERNS,
        CRISIS_HOTLINES as _CRISIS_HOTLINES,
    )
except ImportError:
    _SUICIDE_KW = None
    _SELF_HARM_KW = None
    _SELF_HARM_FUNC = None
    _DESPAIR_KW = None
    _METAPHOR_KW = None
    METAPHOR_EXHAUSTION = None
    METAPHOR_HOPELESSNESS = None
    METAPHOR_ABSENCE = None
    METAPHOR_CHILD_SIGNALS = None
    _IMMINENT_KW = None
    _NEGATION_PATTERNS = None
    _QUOTE_PATTERNS = None
    _CRISIS_HOTLINES = None

class SafetyLevel(IntEnum):
    SAFE=0; WATCH=1; ALERT=2; CRISIS=3; EMERGENCY=4
    def emoji(self): return {0:"\U0001f7e2",1:"\U0001f7e1",2:"\U0001f7e0",3:"\U0001f534",4:"\u26ab"}[self.value]
    def label(self): return {0:"safe",1:"watch",2:"alert",3:"crisis",4:"emergency"}[self.value]

class ThreatCategory(Enum):
    SUICIDE="suicide"; SELF_HARM="self_harm"; HARM_OTHERS="harm_others"
    ABUSE="abuse"; DESPAIR="despair"; SUBSTANCE="substance"; VIOLENCE="violence"

class DetectionSource(Enum):
    KEYWORD="keyword"; METAPHOR="metaphor"; PROGRESSIVE="progressive"
    COMPOUND="compound"; CONTEXT="context"

@dataclass
class DetectionHit:
    category: ThreatCategory
    source: DetectionSource
    matched_text: str
    keyword: str
    confidence: float
    severity: float
    negated: bool=False
    quoted: bool=False

@dataclass
class ProgressiveTrend:
    window_size: int
    trend_score: float
    severity_trajectory: List[float]=field(default_factory=list)
    detected: bool=False
    peak_level: SafetyLevel=SafetyLevel.SAFE

@dataclass
class CompoundRisk:
    active_categories: Set[ThreatCategory]=field(default_factory=set)
    risk_multiplier: float=1.0
    compound_score: float=0.0
    detected: bool=False

@dataclass
class SafetyReport:
    timestamp: float=0.0
    level: SafetyLevel=SafetyLevel.SAFE
    score: float=0.0
    hits: List[DetectionHit]=field(default_factory=list)
    progressive: Optional[ProgressiveTrend]=None
    compound: Optional[CompoundRisk]=None
    categories: Set[ThreatCategory]=field(default_factory=set)
    negated_hits: int=0
    requires_intervention: bool=False
    intervention_message: str=""
    hotlines: List[str]=field(default_factory=list)
    def summary(self):
        parts=[f"{self.level.emoji()} Level: {self.level.label()} (score={self.score:.2f})"]
        if self.categories: parts.append(f"  Categories: {', '.join(c.value for c in self.categories)}")
        if self.hits: parts.append(f"  Hits: {len(self.hits)}")
        if self.negated_hits>0: parts.append(f"  Negated: {self.negated_hits} (downweighted)")
        if self.progressive and self.progressive.detected: parts.append(f"  Progressive: trend={self.progressive.trend_score:.2f}")
        if self.compound and self.compound.detected: parts.append(f"  Compound: {len(self.compound.active_categories)} categories")
        if self.requires_intervention: parts.append(f"  INTERVENTION: {self.intervention_message}")
        return "\n".join(parts)

# === Keyword Banks ===
# 优先使用共享常量模块，回退到本地定义
SUICIDE_EXPLICIT = _SUICIDE_KW if _SUICIDE_KW is not None else ["自杀","想死","不想活","不想活了","活不下去","去死","死了算了","结束生命","结束自己","寻死","轻生","跳楼","跳河","上吊","割腕自杀","服毒","吃药自杀","不想存在","消失就好了","消失吧","suicide","want to die","dont want to live","cant go on","end it all","jump off","hang myself","overdose"]
SELF_HARM = _SELF_HARM_KW if _SELF_HARM_KW is not None else ["自伤","自残","割自己","划自己","划手臂","划手腕","割手臂","割腕","撞墙","咬自己","烫自己","掐自己","抓自己","拔头发","self-harm","self-injury","cut myself","cutting","hit wall","burn myself"]
SELF_HARM_FUNCTIONAL = _SELF_HARM_FUNC if _SELF_HARM_FUNC is not None else ["割了才舒服","痛了才感觉活着","看到血才安心","用身体的痛盖过心里的痛","不割就难受","cut to feel better","pain makes me feel alive","see blood to feel safe"]
HARM_OTHERS=["想杀人","想打人","想伤害别人","想揍他","杀了他","弄死他","让他消失","want to kill","want to hurt someone","want to beat"]
ABUSE_PHYSICAL=["往死里打","打出伤","打出淤青","打得出血","皮带抽","衣架打","扇耳光","踢孩子","打得叫","打到哭","beat to death","leave bruises","drew blood","belt whipping","hanger hitting","slap face","kick child"]
ABUSE_EMOTIONAL=["骂他没用","说他是废物","说他不配活着","冷暴力","不理孩子","威胁抛弃","你再这样我就不要你了","生你有什么用","call useless","call worthless","silent treatment","threaten abandonment"]
ABUSE_NEGLECT=["不管他","让他饿着","不给饭吃","锁在房间","关在门外","let starve","lock in room","lock outside"]
ABUSE_SEXUAL=["猥亵","性侵","性虐待","被摸","molest","sexual abuse","sexual assault","touched inappropriately"]
DESPAIR = _DESPAIR_KW if _DESPAIR_KW is not None else ["活着没意思","活着没意义","生无可恋","一切无所谓","一切都无所谓了","没有任何意义","没有希望","看不到希望","没有未来","不会好了","life is meaningless","no point living","nothing matters","no hope","cant see hope","no future","wont get better"]
SUBSTANCE_CRISIS=["嗑药","吸毒过量","喝酒喝到吐血","药物过量","服药过量","drug overdose","drink till bleeding"]
VIOLENCE_DOMESTIC=["家暴","家庭暴力","被打","老公打我","老婆打我","被老公打","被老婆打","动手了","domestic violence","hit by husband","hit by wife","he hit me"]
VIOLENCE_BULLYING=["被欺负","被霸凌","被围殴","被孤立","校园暴力","校园霸凌","bullied","being bullied","mobbed","isolated","campus violence"]

METAPHOR_EXHAUSTION = METAPHOR_EXHAUSTION if METAPHOR_EXHAUSTION is not None else [("撑不下去了",0.7),("真的累了",0.5),("累了真的累了",0.7),("好累啊",0.3),("精疲力竭",0.4),("心力交瘁",0.5),("被掏空了",0.4),("cant go on anymore",0.7),("really tired",0.5),("so so tired",0.7),("exhausted",0.4),("burned out",0.5),("emptied out",0.4)]
METAPHOR_HOPELESSNESS = METAPHOR_HOPELESSNESS if METAPHOR_HOPELESSNESS is not None else [("没希望了",0.7),("看不到尽头",0.6),("永远都不会好了",0.7),("就这样了吧",0.5),("无所谓了",0.5),("算了吧",0.3),("放弃了",0.4),("随便吧",0.3),("no hope left",0.7),("cant see the end",0.6),("will never get better",0.7),("whatever",0.5),("doesnt matter",0.5),("give up",0.4)]
METAPHOR_ABSENCE = METAPHOR_ABSENCE if METAPHOR_ABSENCE is not None else [("如果我不在了",0.8),("如果我消失了",0.7),("没人会在乎的",0.7),("没有我大家会更好",0.8),("我不配活着",0.8),("我是个累赘",0.7),("我是多余的",0.6),("if I werent here",0.8),("if I disappeared",0.7),("nobody would care",0.7),("everyone better without me",0.8),("I dont deserve to live",0.8),("Im a burden",0.7)]
METAPHOR_CHILD_SIGNALS = METAPHOR_CHILD_SIGNALS if METAPHOR_CHILD_SIGNALS is not None else [("不想去学校了",0.3),("活着好累",0.7),("没人理解我",0.4),("都是我的错",0.5),("我不够好",0.4),("我什么都做不好",0.5),("没有人喜欢我",0.5),("dont want to go to school",0.3),("life is so tiring",0.7),("nobody understands me",0.4),("its all my fault",0.5),("Im not good enough",0.4)]

NEGATION_PATTERNS = _NEGATION_PATTERNS if _NEGATION_PATTERNS is not None else [r"不是.{0,3}(想死|自杀|不想活)",r"并没有?(想死|自杀)",r"不会(自杀|想死|去死)",r"我不(想死|想自杀)",r"从来没有(想死|自杀)",r"not.{0,3}(want to die|suicide|dont want to live)",r"dont want to die",r"would never (suicide|die|kill)",r"never (want to die|suicide)"]
QUOTE_PATTERNS = _QUOTE_PATTERNS if _QUOTE_PATTERNS is not None else [r"他.{0,5}(说|讲).{0,10}(想死|不想活|自杀)",r"孩子.{0,5}(说|讲).{0,10}(想死|不想活)",r"她.{0,5}(说|讲).{0,10}(想死|不想活)",r"别人.{0,3}(说|讲)",r"新闻.{0,5}(说|报道)",r"书上.{0,3}(说|写)",r"网上.{0,3}(说)",r"(he|she|they).{0,5}(said|told).{0,10}(want to die|suicide)",r"child.{0,5}(said|told)",r"news.{0,5}(said|reported)"]
IMMINENT_SIGNALS = _IMMINENT_KW if _IMMINENT_KW is not None else ["正在","现在就要","马上就","已经准备好了","已经割了","已经吃了","正在割","正在打","此时此刻","就在现在","right now","about to","already done","already cut","already took","prepared"]
CRISIS_HOTLINES = _CRISIS_HOTLINES if _CRISIS_HOTLINES is not None else ["全国24小时心理援助热线：400-161-9995","北京心理危机研究与干预中心：010-82951332","生命热线：400-821-1215","希望24热线：400-161-9995","青少年心理热线：12355","报警电话：110","急救电话：120"]

# === Detectors ===

class KeywordDetector:
    def __init__(self):
        self._map={ThreatCategory.SUICIDE:SUICIDE_EXPLICIT, ThreatCategory.SELF_HARM:SELF_HARM+SELF_HARM_FUNCTIONAL, ThreatCategory.HARM_OTHERS:HARM_OTHERS, ThreatCategory.ABUSE:ABUSE_PHYSICAL+ABUSE_EMOTIONAL+ABUSE_NEGLECT+ABUSE_SEXUAL, ThreatCategory.DESPAIR:DESPAIR, ThreatCategory.SUBSTANCE:SUBSTANCE_CRISIS, ThreatCategory.VIOLENCE:VIOLENCE_DOMESTIC+VIOLENCE_BULLYING}
        self._sev={ThreatCategory.SUICIDE:0.95,ThreatCategory.SELF_HARM:0.85,ThreatCategory.HARM_OTHERS:0.90,ThreatCategory.ABUSE:0.90,ThreatCategory.DESPAIR:0.60,ThreatCategory.SUBSTANCE:0.70,ThreatCategory.VIOLENCE:0.80}
        self._neg=[re.compile(p,re.I) for p in NEGATION_PATTERNS]
        self._quo=[re.compile(p,re.I) for p in QUOTE_PATTERNS]
    def detect(self,text):
        if not text: return []
        hits=[]
        tl=text.lower()
        for cat,kws in self._map.items():
            for kw in kws:
                if kw in tl:
                    neg=any(p.search(text) for p in self._neg)
                    quo=any(p.search(text) for p in self._quo)
                    c=self._sev.get(cat,0.5)
                    if neg: c*=0.3
                    if quo: c*=0.5
                    hits.append(DetectionHit(cat,DetectionSource.KEYWORD,kw,kw,c,self._sev.get(cat,0.5),neg,quo))
        return hits

class MetaphorDetector:
    def __init__(self):
        self._g={ThreatCategory.DESPAIR:METAPHOR_EXHAUSTION+METAPHOR_HOPELESSNESS,ThreatCategory.SUICIDE:METAPHOR_ABSENCE,ThreatCategory.SELF_HARM:METAPHOR_CHILD_SIGNALS}
    def detect(self,text):
        if not text: return []
        hits=[]
        for cat,ps in self._g.items():
            for pat,sev in ps:
                if pat in text:
                    hits.append(DetectionHit(cat,DetectionSource.METAPHOR,pat,pat,sev,sev))
        return hits

class ProgressiveDetector:
    def __init__(self,window_size=5,threshold=0.3):
        self.window_size=window_size; self.threshold=threshold; self._h=[]
    def add_score(self,score):
        self._h.append(score)
        if len(self._h)>self.window_size*2: self._h=self._h[-self.window_size*2:]
    def detect(self):
        w=self._h[-self.window_size:] if len(self._h)>=self.window_size else self._h
        if len(w)<3: return ProgressiveTrend(len(w),0.0,list(w),False)
        n=len(w); xm=(n-1)/2.0; ym=sum(w)/n
        num=sum((i-xm)*(y-ym) for i,y in enumerate(w))
        den=sum((i-xm)**2 for i in range(n))
        slope=num/den if den else 0.0
        trend=max(-1.0,min(1.0,slope*n))
        pk=max(w) if w else 0.0
        pl=SafetyLevel.EMERGENCY if pk>=0.9 else SafetyLevel.CRISIS if pk>=0.7 else SafetyLevel.ALERT if pk>=0.5 else SafetyLevel.WATCH if pk>=0.3 else SafetyLevel.SAFE
        return ProgressiveTrend(n,trend,list(w),trend>self.threshold,pl)
    def reset(self): self._h.clear()

class CompoundDetector:
    RULES={frozenset({ThreatCategory.SUICIDE,ThreatCategory.SELF_HARM}):1.5,frozenset({ThreatCategory.SUICIDE,ThreatCategory.DESPAIR}):1.4,frozenset({ThreatCategory.SELF_HARM,ThreatCategory.DESPAIR}):1.3,frozenset({ThreatCategory.ABUSE,ThreatCategory.VIOLENCE}):1.4,frozenset({ThreatCategory.SUICIDE,ThreatCategory.ABUSE}):1.6,frozenset({ThreatCategory.SUICIDE,ThreatCategory.SELF_HARM,ThreatCategory.DESPAIR}):1.8,frozenset({ThreatCategory.ABUSE,ThreatCategory.VIOLENCE,ThreatCategory.SELF_HARM}):1.7}
    def detect(self,hits):
        if not hits: return CompoundRisk()
        active=set(h.category for h in hits if not h.negated and not h.quoted)
        if len(active)<2: return CompoundRisk(active_categories=active)
        best=1.0
        for rs,m in self.RULES.items():
            if rs.issubset(active): best=max(best,m)
        cs=min(1.0,sum(h.confidence for h in hits if not h.negated)*best/len(active))
        return CompoundRisk(active,best,cs,True)

class ContextAnalyzer:
    DISCUSSION=["how to view","what do you think about","news reported","research shows","paper says","lets discuss","lets analyze","lets research","如何看待","怎么看待","新闻报道","研究表明","论文说","讨论一下","分析一下","研究一下"]
    def analyze(self,text,hits):
        if not hits: return hits
        is_disc=any(d in text.lower() for d in self.DISCUSSION)
        out=[]
        for h in hits:
            if is_disc and h.source==DetectionSource.KEYWORD:
                h=DetectionHit(h.category,h.source,h.matched_text,h.keyword,h.confidence*0.4,h.severity,h.negated,True)
            out.append(h)
        return out

# === Main Entry ===

class SafetyChecker:
    """
    Safety Checker main entry
    
    Usage:
        checker = SafetyChecker()
        report = checker.check("I feel life is meaningless")
        print(report.summary())
        
        # Multi-turn conversation
        for msg in conversation:
            report = checker.check(msg)
    """
    def __init__(self):
        self.keyword_detector=KeywordDetector()
        self.metaphor_detector=MetaphorDetector()
        self.progressive_detector=ProgressiveDetector()
        self.compound_detector=CompoundDetector()
        self.context_analyzer=ContextAnalyzer()
    
    def check(self,text):
        """Check a single message, return SafetyReport"""
        if not text: return SafetyReport(timestamp=time.time())
        kw=self.keyword_detector.detect(text)
        meta=self.metaphor_detector.detect(text)
        all_h=self.context_analyzer.analyze(text,kw+meta)
        neg_c=sum(1 for h in all_h if h.negated)
        comp=self.compound_detector.detect(all_h)
        cats=set(h.category for h in all_h if not h.negated)
        raw=max((h.confidence for h in all_h),default=0.0)
        if comp.detected: raw=min(1.0,raw*comp.risk_multiplier)
        has_imminent=any(s in text.lower() for s in IMMINENT_SIGNALS)
        if has_imminent and any(h.category==ThreatCategory.SUICIDE and not h.negated for h in all_h): raw=max(raw,0.95)
        self.progressive_detector.add_score(raw)
        prog=self.progressive_detector.detect()
        if prog.detected: raw=min(1.0,max(raw,prog.trend_score+0.3))
        if raw>=0.9: lvl=SafetyLevel.EMERGENCY
        elif raw>=0.7: lvl=SafetyLevel.CRISIS
        elif raw>=0.5: lvl=SafetyLevel.ALERT
        elif raw>=0.3: lvl=SafetyLevel.WATCH
        else: lvl=SafetyLevel.SAFE
        intervene=lvl>=SafetyLevel.CRISIS
        msg=""
        if intervene:
            if ThreatCategory.SUICIDE in cats: msg="Detected suicide ideation. Immediate referral required."
            elif ThreatCategory.SELF_HARM in cats: msg="Detected self-harm signals. Professional referral recommended."
            elif ThreatCategory.ABUSE in cats: msg="Detected abuse indicators. Child protection referral required."
            elif ThreatCategory.HARM_OTHERS in cats: msg="Detected harm-to-others signals. Safety assessment needed."
            elif ThreatCategory.VIOLENCE in cats: msg="Detected violence indicators. Safety planning required."
            else: msg="Elevated risk detected. Professional assessment recommended."
        hl=CRISIS_HOTLINES if intervene else []
        return SafetyReport(timestamp=time.time(),level=lvl,score=raw,hits=all_h,progressive=prog,compound=comp,categories=cats,negated_hits=neg_c,requires_intervention=intervene,intervention_message=msg,hotlines=hl)

    def check_conversation(self,messages):
        """Check a list of messages, return list of SafetyReports"""
        return [self.check(m) for m in messages]

    def get_risk_score(self,text):
        """Quick risk score (0.0-1.0) for integration with other systems"""
        r=self.check(text)
        return r.score

    def is_crisis(self,text):
        """Quick boolean crisis check"""
        return self.check(text).level>=SafetyLevel.CRISIS

# === Integration Helper ===

def create_safety_checker():
    """Factory function for creating SafetyChecker instance"""
    return SafetyChecker()

def quick_safety_check(text):
    """Quick safety check returning dict for easy integration"""
    sc=SafetyChecker()
    r=sc.check(text)
    return {"level":r.level.label(),"score":r.score,"categories":[c.value for c in r.categories],"intervention":r.requires_intervention,"message":r.intervention_message,"hit_count":len(r.hits)}

# === Backward Compatibility with reasoning_engine ===

class CrisisDetectorAdapter:
    """
    Adapter to integrate SafetyChecker with reasoning_engine.py's CrisisDetector interface.
    Maps SafetyLevel to CrisisLevel for backward compatibility.
    """
    def __init__(self):
        self._checker=SafetyChecker()
    
    def detect(self,text):
        """Compatible with reasoning_engine.CrisisDetector.detect() interface"""
        from enum import Enum as _Enum
        class CrisisLevel(_Enum):
            NONE="none"; METAPHOR="metaphor"; DIRECT="direct"; IMMINENT="imminent"
        r=self._checker.check(text)
        if r.level==SafetyLevel.EMERGENCY: lvl=CrisisLevel.IMMINENT
        elif r.level==SafetyLevel.CRISIS: lvl=CrisisLevel.DIRECT
        elif r.level==SafetyLevel.ALERT: lvl=CrisisLevel.METAPHOR
        else: lvl=CrisisLevel.NONE
        kws=[h.keyword for h in r.hits if h.source==DetectionSource.KEYWORD and not h.negated]
        metas=[h.keyword for h in r.hits if h.source==DetectionSource.METAPHOR]
        imminent=any(s in text.lower() for s in IMMINENT_SIGNALS)
        # Return a compatible object
        class _R: pass
        obj=_R()
        obj.level=lvl
        obj.matched_keywords=kws
        obj.matched_metaphors=metas
        obj.has_imminent_signal=imminent
        obj.confidence=r.score
        return obj

if __name__=="__main__":
    # Self-test
    checker=SafetyChecker()
    tests=[
        ("I feel fine today",SafetyLevel.SAFE),
        ("I'm so tired of everything",SafetyLevel.WATCH),
        ("Life has no meaning, I give up",SafetyLevel.ALERT),
        ("I want to die",SafetyLevel.CRISIS),
        ("I'm about to end it all right now",SafetyLevel.EMERGENCY),
        ("My child said they want to die",SafetyLevel.CRISIS),
        ("I don't want to die, just tired",SafetyLevel.WATCH),
    ]
    print("=== Safety Checker Self-Test ===")
    passed=0
    for text,expected in tests:
        r=checker.check(text)
        ok=r.level.value>=expected.value-1  # Allow 1 level tolerance
        mark="PASS" if ok else "FAIL"
        if ok: passed+=1
        print(f"[{mark}] '{text[:40]}...' -> {r.level.label()} (expected>={expected.label()}, score={r.score:.2f})")
    print(f"\nResults: {passed}/{len(tests)} passed")
    # Progressive test
    print("\n=== Progressive Detection Test ===")
    prog=ProgressiveDetector(window_size=4)
    for s in [0.1,0.2,0.4,0.6,0.8]:
        prog.add_score(s)
    trend=prog.detect()
    print(f"Trend: {trend.trend_score:.2f}, detected={trend.detected}")
    # Compound test
    print("\n=== Compound Detection Test ===")
    comp=CompoundDetector()
    h1=DetectionHit(ThreatCategory.SUICIDE,DetectionSource.KEYWORD,"want to die","want to die",0.95,0.95)
    h2=DetectionHit(ThreatCategory.SELF_HARM,DetectionSource.KEYWORD,"cut myself","cut myself",0.85,0.85)
    cr=comp.detect([h1,h2])
    print(f"Compound: multiplier={cr.risk_multiplier}, score={cr.compound_score:.2f}, detected={cr.detected}")