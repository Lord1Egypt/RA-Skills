#!/usr/bin/env python3
"""CNexus 2.0 Web UI -- full Shell + Float frontend"""

import os, sys, json, time, math, traceback, cgi, tempfile
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src import CNexusOSCoreEngine

_engine = None
def get_engine():
    global _engine
    if _engine is None:
        _engine = CNexusOSCoreEngine()
        _engine.initialize()
    return _engine

def api_status():
    e = get_engine(); k = e.kernel
    st = k.status() if hasattr(k, "status") else {"active": False}
    st["engine_initialized"] = e.is_initialized
    st["memory_count"] = k.state.get("memory_count", 0)
    st["execution_count"] = k.state.get("execution_count", 0)
    st["current_iteration"] = k.cog.get("iteration", 0)
    return st

def api_converse(text):
    e = get_engine()
    try:
        reply = e.handle_request(text)
    except Exception as ex:
        reply = '[stub] 已收到: ' + text[:80]
        # Still try to write to memory_store directly so memory_dump works
        k = e.kernel
        import hashlib
        mem_id = hashlib.md5(text.encode()).hexdigest()[:8]
        k.memory_store[mem_id] = {
            'block_id': mem_id, 'type': 'memory_block',
            'skill': 'upload', 'input': text,
            'content': {'input': text, 'skill': 'upload', 'output_hash': ''},
            'metadata': {'timestamp_boot': k.state.get('boot_time', 0), 'iteration': k.cog.get('iteration', 0), 'strategy': 'upload'},
            'weight': 0.7, 'decay_factor': 1.0, 'reference_count': 0
        }
        k.state['memory_count'] = k.state.get('memory_count', 0) + 1
    k = e.kernel
    return {'reply':reply,'cog_state':k.cog.get('cog_state',{}),
        'memory_count':k.state.get('memory_count',0),
        'execution_count':k.state.get('execution_count',0),
        'iteration':k.cog.get('iteration',0),
        'trace':k.cog.get('trace',[]),
        'execution_history':k.execution_history[-5:] if hasattr(k,'execution_history') else []}

def api_memory_dump(limit=20):
    e = get_engine(); k = e.kernel
    if hasattr(k,'memory_dump'): return k.memory_dump(limit)
    keys=sorted(k.memory_store.keys(),key=lambda kk:kk,reverse=True); entries=[]
    for kk in keys[:limit]:
        blk=k.memory_store[kk]; entries.append({
            'block_id':blk.get('block_id',kk),'type':blk.get('type',''),
            'skill':blk.get('content',{}).get('skill',''),
            'input':blk.get('content',{}).get('input','')[:60],
            'weight':blk.get('weight',0),
            'iteration':blk.get('metadata',{}).get('iteration',0)})
    return {'total_entries':len(k.memory_store),'entries':entries}

def api_exec_trace(limit=30):
    e=get_engine(); k=e.kernel
    h=getattr(k,'execution_history',[]); return {'traces':h[-limit:],'total':len(h)}

def api_cog_state():
    e=get_engine(); k=e.kernel
    return {'cog_state':k.cog.get('cog_state',{}),
        'state':k.state,'iteration':k.cog.get('iteration',0),
        'skills_loaded':len(getattr(k,'skills',{})),
        'skill_registry':list(getattr(k,'skill_registry',{}).keys())[:12],
        'execution_history_count':len(getattr(k,'execution_history',[]))}

def api_skill_graph():
    e=get_engine(); k=e.kernel
    return {'skills':list(k.skills.keys()),
        'skill_graph':k.skill_graph,'classification':k.classification}

def api_reset():
    e=get_engine(); k=e.kernel
    return k.reset() if hasattr(k,'reset') else {'status':'error'}

# === SHELL_HTML ===


SHELL_HTML = r''''''

# === FLOAT ===
FLOAT_HTML = r''''''


# === HTTP Handler ===
class CNexusUIHandler(BaseHTTPRequestHandler):
    def _json(self, data, st=200):
        self.send_response(st)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        self.wfile.write(json.dumps(data,ensure_ascii=False,default=str).encode('utf-8'))

    def _html(self, s, st=200):
        self.send_response(st)
        self.send_header('Content-Type','text/html; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        self.wfile.write(s.encode('utf-8'))

    def do_POST(self):
        p = urlparse(self.path); path = p.path.rstrip('/') or '/'
        try:
            length = int(self.headers.get('Content-Length',0))
            body = self.rfile.read(length) if length else b'{}'
            if path == '/api/upload':
                ct = self.headers.get('Content-Type','')
                if 'multipart/form-data' in ct:
                    # Parse multipart manually — simpler than cgi.FieldStorage
                    import re
                    results = []; ok = 0
                    boundary = ct.split('boundary=')[-1].strip().strip('"')
                    parts = body.split(('--' + boundary).encode())
                    for part in parts:
                        if not part or part == b'--\r\n' or part == b'--' or part == b'\r\n':
                            continue
                        # Split headers from body at first \r\n\r\n
                        hdr_end = part.find(b'\r\n\r\n')
                        if hdr_end < 0: continue
                        hdrs_raw = part[:hdr_end].decode('utf-8', errors='replace')
                        data_raw = part[hdr_end+4:]
                        # Strip trailing \r\n--\r\n etc
                        if data_raw.endswith(b'\r\n'):
                            data_raw = data_raw[:-2]
                        if data_raw.endswith(b'--'):
                            data_raw = data_raw[:-2]
                        if data_raw.endswith(b'\r\n'):
                            data_raw = data_raw[:-2]
                        # Get filename from Content-Disposition
                        fn_match = re.search(r'filename="([^"]*)"', hdrs_raw)
                        if not fn_match:
                            continue
                        filename = fn_match.group(1)
                        try:
                            text_data = data_raw.decode('utf-8')[:5000]
                        except:
                            text_data = '[binary file: ' + filename + ' — size: ' + str(len(data_raw)) + ' bytes]'
                        text_content = '-- file: ' + filename + ' --\n' + text_data
                        try:
                            resp = api_converse(text_content.strip())
                            ok += 1
                            results.append({'file': filename, 'status': 'ok', 'reply_len': len(str(resp.get('reply',''))) if isinstance(resp,dict) else 0})
                        except Exception as e:
                            results.append({'file': filename, 'status': 'error', 'message': str(e)})
                    return self._json({'ok':True,'count':ok,'imported_blocks_count':ok,'results':results})
                else:
                    text = body.decode('utf-8',errors='replace')
                    try:
                        resp = api_converse(text)
                        return self._json({'ok':True,'status':'success','reply':resp.get('reply','') if isinstance(resp,dict) else str(resp)})
                    except Exception as e:
                        return self._json({'ok':False,'error':str(e)},500)
            if path == '/api/converse':
                t = json.loads(body).get('text','')
                return self._json({'error':'missing text'},400) if not t else self._json(api_converse(t))
            return self._json({'error':'not found','path':path},404)
        except Exception as e:
            return self._json({'error':str(e),'trace':traceback.format_exc()},500)
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Methods','GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers','Content-Type, Authorization, X-Requested-With')
        self.send_header('Access-Control-Max-Age','86400')
        self.end_headers()

    def do_GET(self):
        p = urlparse(self.path); path = p.path.rstrip('/') or '/'; qs = parse_qs(p.query)
        try:
            if path in ('/','/shell'): return self._html(SHELL_HTML)
            if path == '/float': return self._html(FLOAT_HTML)
            if path == '/api/status': return self._json(api_status())
            if path == '/api/converse':
                t = qs.get('text',[''])[0]
                return self._json({'error':'missing text'},400) if not t else self._json(api_converse(t))
            if path == '/api/memory_dump':
                return self._json(api_memory_dump(int(qs.get('limit',['20'])[0])))
            if path == '/api/exec_trace':
                return self._json(api_exec_trace(int(qs.get('limit',['30'])[0])))
            if path == '/api/cog_state': return self._json(api_cog_state())
            if path == '/api/skill_graph': return self._json(api_skill_graph())
            if path == '/api/reset': return self._json(api_reset())
            self.send_response(404); self.end_headers(); self.wfile.write(b'404')
        except Exception as e:
            self._json({'error':str(e),'trace':traceback.format_exc()},500) if path.startswith('/api') else self._html('404 not found')

    def log_message(self, *a): pass

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--host',default='127.0.0.1')
    ap.add_argument('--port',type=int,default=7862)
    ap.add_argument('--no-engine',action='store_true')
    args = ap.parse_args()

    if not args.no_engine:
        print('[CNexus 2.0] init kernel...')
        try:
            get_engine()
            e = get_engine()
            print(f'[CNexus 2.0] ready | memory: {len(e.kernel.memory_store)} | exec: {e.kernel.state["execution_count"]}')
        except Exception as ex:
            print(f'[CNexus 2.0] init failed (UI still works): {ex}')

    server = HTTPServer((args.host,args.port),CNexusUIHandler)
    print(f'\n  CNexus 2.0 Console -> http://{args.host}:{args.port}')
    print(f'  Float -> http://{args.host}:{args.port}/float')
    print()
    try: server.serve_forever()
    except KeyboardInterrupt: print('\n[CNexus 2.0] shutdown'); server.server_close()
