import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from audit_workflow_security import audit,masked_url

def node(nid,typ,**values):
    return {'nodeId':nid,'flowNodeType':typ,'inputs':[{'key':k,'value':v} for k,v in values.items()]}
def workflow(*nodes):return {'nodes':list(nodes),'edges':[]}
def rules(w,**kw):return {x['rule'] for x in audit(w,**kw)['findings']}

class SecurityAudit(unittest.TestCase):
    def test_no_execution_of_supplied_code(self):
        with tempfile.TemporaryDirectory() as d:
            marker=Path(d)/'marker'
            w=workflow(node('untrusted','code',code=f"__import__('pathlib').Path({str(marker)!r}).write_text('executed')"))
            audit(w);self.assertFalse(marker.exists())
    def test_secret_header_redacted(self):
        w=workflow(node('h','httpRequest468',system_httpReqUrl='https://example.org/hook/SENSITIVEPATH?key=SENSITIVEQUERY',system_httpHeader=[{'key':'Authorization','value':'Bearer PRIVATESECRET123456789'}]))
        r=audit(w);text=json.dumps(r);self.assertIn('SEC001',rules(w))
        for secret in ['PRIVATESECRET','SENSITIVEPATH','SENSITIVEQUERY']:self.assertNotIn(secret,text)
    def test_managed_credential_not_plain_secret(self):
        w=workflow(node('h','httpRequest468',system_httpReqUrl='https://example.org/',system_header_secret={'a':{'secret':'opaqueprotectedvalue'}}))
        self.assertNotIn('SEC001',rules(w));self.assertNotIn('opaqueprotectedvalue',json.dumps(audit(w)))
    def test_reference_header_not_literal(self):
        w=workflow(node('h','httpRequest468',system_httpReqUrl='https://example.org/',system_httpHeader=[{'key':'Authorization','value':'{{$VARIABLE_NODE_ID.key$}}'}]))
        self.assertNotIn('SEC001',rules(w))
    def test_dynamic_url_no_request(self):
        self.assertIn('SEC011',rules(workflow(node('h','httpRequest468',system_httpReqUrl='{{$s.url$}}'))))
    def test_plain_http_and_missing_auth_are_observations(self):
        r=rules(workflow(node('h','httpRequest468',system_httpReqUrl='http://192.0.2.1/ping')))
        self.assertTrue({'SEC012','SEC013'}<=r)
    def test_policy_exact_host(self):
        w=workflow(node('h','httpRequest468',system_httpReqUrl='https://api.example.org/x'))
        self.assertNotIn('SEC015',rules(w,allowed_hosts={'api.example.org'}))
        self.assertIn('SEC015',rules(w,allowed_hosts={'example.org'}))
    def test_only_http_node_url_is_sink(self):
        r=audit(workflow(node('guide','code',code="return 'https://example.org/howto';")))
        self.assertEqual(r['summary']['http_nodes'],0)
    def test_dynamic_execution_pattern_is_not_verdict(self):
        r=audit(workflow(node('c','code',code="eval('1+1')")))
        self.assertTrue(any(x['rule']=='SEC030' and x['confidence']=='review_required' for x in r['findings']))
    def test_model_data_refs(self):
        w=workflow(node('s','workflowStart'),node('m','chatNode',fileUrlList=['s','files'],aiChatVision=True,userChatInput='{{$s.userChatInput$}}'))
        r=audit(w);self.assertTrue(r['inventory']['models'][0]['vision']);self.assertTrue(r['reference_edges'])
    def test_url_credentials_never_returned(self):
        text=json.dumps(masked_url('https://someone:PRIVATEPASS@example.org/a?token=QUERYSECRET#SECRETFRAGMENT'))
        for secret in ['someone','PRIVATEPASS','QUERYSECRET','SECRETFRAGMENT']:self.assertNotIn(secret,text)
    def test_structural_reachability_not_all_paths(self):
        w=workflow(node('s','workflowStart'),node('h','httpRequest468',system_httpReqUrl='https://example.org'))
        self.assertFalse(audit(w)['inventory']['http'][0]['structurally_reachable'])
    def test_invalid_shape(self):
        with self.assertRaises(ValueError):audit({'nodes':[]})

if __name__=='__main__':unittest.main()
