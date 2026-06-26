#!/usr/bin/env python3
import argparse,json,subprocess,sys
from pathlib import Path
from datetime import datetime,UTC
p=argparse.ArgumentParser();p.add_argument("--task",required=True);p.add_argument("--context",default="");p.add_argument("--constraints",default="");a=p.parse_args()
ws=Path("/home/jason/.openclaw/workspace");t=(ws/a.task).resolve() if not Path(a.task).is_absolute() else Path(a.task).resolve()
t.exists() or (print(json.dumps({"skill":"AI_AutoTester","status":"error","error":f"Target path not found: {t}"},ensure_ascii=False,indent=2)),sys.exit(1))
(td:=t/"tests").mkdir(parents=True,exist_ok=True)
(tf:=td/"test_smoke.py").exists() or tf.write_text('from app.main import app\nfrom fastapi.testclient import TestClient\n\ndef test_root():\n c=TestClient(app)\n r=c.get("/")\n assert r.status_code==200\n',encoding="utf-8")
(r1:=t/"requirements.txt").exists() and subprocess.run(["python","-m","pip","install","-q","-r",str(r1)],cwd=str(t),check=False)
(t/"requirements-test.txt").write_text("pytest==8.3.2\nhttpx==0.27.2\n",encoding="utf-8")
subprocess.run(["python","-m","pip","install","-q","-r",str(t/"requirements-test.txt")],cwd=str(t),check=False)
r=subprocess.run(["python","-m","pytest","-q"],cwd=str(t),capture_output=True,text=True)
print(json.dumps({"skill":"AI_AutoTester","status":"ok" if r.returncode==0 else "failed","task":a.task,"target":str(t),"returncode":r.returncode,"stdout":r.stdout[-4000:],"stderr":r.stderr[-2000:],"timestamp":datetime.now(UTC).isoformat().replace("+00:00","Z")},ensure_ascii=False,indent=2))
sys.exit(0 if r.returncode==0 else 2)
