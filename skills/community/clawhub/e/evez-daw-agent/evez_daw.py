#!/usr/bin/env python3
"""EVEZ DAW Agent - Breakcore/Dubstep/Phonk/Distortion/404"""

import json, time, math, os, logging
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import numpy as np
import soundfile as sf
from scipy import signal

BASE_DIR = Path(__file__).parent
SR = 44100
PI2 = 2 * math.pi

def mt(s): return int(s * SR)
def norm(a, t=0.9): p=np.max(np.abs(a)); return a*(t/p) if p>0 else a
def fad(a, fi=0.005, fo=0.01):
    r=a.copy(); i=mt(fi); o=mt(fo)
    if 0<i<len(r): r[:i]*=np.linspace(0,1,i)
    if 0<o<len(r): r[-o:]*=np.linspace(1,0,o)
    return r

def bflt(a, lo, hi, order=4, bt='band'):
    ny=SR/2; lo=max(20,min(lo,ny-100)); hi=max(lo+100,min(hi,ny-1))
    sos=signal.butter(order,[lo/ny,hi/ny],btype=bt,output='sos')
    return signal.sosfilt(sos,a).astype(np.float32)

# ── DRUMS ──
def synth_kick(dur=0.5, freq=55, dec=8.0, click=0.02):
    t=np.linspace(0,dur,mt(dur),dtype=np.float32)
    pe=np.exp(-dec*t)*(freq*4-freq)+freq; ph=np.cumsum(pe/SR)*PI2
    body=np.sin(ph)*np.exp(-dec*t)
    cl=mt(click); ct=np.linspace(0,click,cl,dtype=np.float32)
    cw=np.sin(PI2*2000*ct)*np.exp(-60*ct)
    r=np.zeros(len(t),dtype=np.float32); r[:cl]+=cw*0.3; r+=body
    return fad(norm(r))

def synth_snare(dur=0.3, freq=200, nm=0.7):
    t=np.linspace(0,dur,mt(dur),dtype=np.float32)
    body=np.sin(PI2*freq*t)*np.exp(-20*t)
    noise=np.random.uniform(-1,1,len(t)).astype(np.float32)*np.exp(-12*t)
    res=np.sin(PI2*freq*3*t)*np.exp(-30*t)*0.3
    return fad(norm((1-nm)*body+nm*noise+res))

def synth_hat(dur=0.1, freq=8000, dec=40, open=False):
    if open: dur=0.3; dec=12
    t=np.linspace(0,dur,mt(dur),dtype=np.float32)
    h1=np.sin(PI2*freq*t); h2=np.sin(PI2*freq*1.5*t)*0.5
    h3=np.sin(PI2*freq*2.3*t)*0.3; h4=np.sin(PI2*freq*3.1*t)*0.2
    met=(h1+h2+h3+h4)*0.25
    noise=np.random.uniform(-1,1,len(t)).astype(np.float32)*0.5
    r=(met+noise)*np.exp(-dec*t)
    return fad(norm(bflt(r,6000,14000)))

def synth_clap(dur=0.15, layers=4):
    r=np.zeros(mt(dur),dtype=np.float32)
    for i in range(layers):
        off=int(i*0.008*SR); bl=mt(0.02)
        b=np.random.uniform(-1,1,bl).astype(np.float32)*np.exp(-80*np.linspace(0,0.02,bl))
        end=min(off+bl,len(r)); r[off:end]+=b[:end-off]
    return fad(norm(r*np.exp(-18*np.linspace(0,dur,len(r)))))

def synth_rim(dur=0.05, freq=1000):
    t=np.linspace(0,dur,mt(dur),dtype=np.float32)
    return fad(norm(np.sin(PI2*freq*t)*np.exp(-80*t)*0.3+np.random.uniform(-1,1,len(t)).astype(np.float32)*np.exp(-100*t)*0.7))

# ── BASS ──
def synth_sub(dur, freq=40):
    t=np.linspace(0,dur,mt(dur),dtype=np.float32); return fad(norm(np.sin(PI2*freq*t)))

def synth_reese(dur, freq=55, det=8):
    t=np.linspace(0,dur,mt(dur),dtype=np.float32)
    return fad(norm((np.sin(PI2*freq*t)+np.sin(PI2*(freq+det)*t)*0.8+np.sin(PI2*(freq-det*0.5)*t)*0.6)/2.4))

def synth_wobble(dur, freq=55, lfo_r=4, lfo_d=800):
    t=np.linspace(0,dur,mt(dur),dtype=np.float32)
    src=norm(np.sin(PI2*freq*t)+0.5*np.sin(PI2*freq*2*t)+0.3*np.sin(PI2*freq*3*t))
    lfo=(np.sin(PI2*lfo_r*t)+1)/2; cutoff=200+lfo*lfo_d
    r=np.zeros_like(src)
    for i in range(0,len(src),256):
        e=min(i+256,len(src)); c=int(cutoff[i])
        r[i:e]=bflt(src[i:e],max(100,c-500),min(20000,c+500))
    return fad(norm(r))

def synth_phonk_bass(dur, freq=65, dist=3.0):
    t=np.linspace(0,dur,mt(dur),dtype=np.float32)
    pe=np.exp(-3*t)*(freq*2-freq)+freq; ph=np.cumsum(pe/SR)*PI2
    body=np.sin(ph)*np.exp(-2*t); body=np.tanh(body*dist)/np.tanh(dist)
    sub=np.sin(PI2*freq*0.5*t)*np.exp(-1.5*t)*0.5
    return fad(norm(body+sub),0.002,0.05)

def synth_scream(dur, freq=80):
    t=np.linspace(0,dur,mt(dur),dtype=np.float32)
    harm=sum(np.sin(PI2*freq*n*t)/n for n in range(1,12)); harm=norm(harm)
    r=np.sin(PI2*freq*t+harm*3); r=np.tanh(r*5)/np.tanh(5)
    return fad(norm(r))

# ── FX ──
def fx_dist(a, drive=3.0, mix=1.0):
    d=np.tanh(a*drive)/np.tanh(drive); return (1-mix)*a+mix*d

def fx_crush(a, bits=8, ds=4):
    lv=2**bits; c=np.round(a*lv)/lv
    if ds>1: idx=np.arange(len(c)); c=np.interp(idx,idx[::ds],c[::ds]).astype(np.float32)
    return c

def fx_reverb(a, dec=0.5, dms=50, wet=0.3):
    r=a.copy(); ds=int(dms*SR/1000)
    for i in range(1,7):
        off=int(ds*(1+i*0.37)); g=(dec**i)*wet
        if off<len(r): r[off:]+=a[:len(r)-off]*g
    return norm(r)

def fx_delay(a, dms=250, fb=0.4, wet=0.3):
    ds=int(dms*SR/1000); r=a.copy(); c=a
    for i in range(1,6):
        g=fb**i*wet; s=np.zeros(len(r),dtype=np.float32); off=ds*i
        if off<len(c): s[off:off+len(c)]=c[:len(c)-off]*g; r+=s; c=s
    return norm(r)

def fx_lp(a, cut=2000, res=5):
    ny=cut/(SR/2); ny=max(0.01,min(0.99,ny))
    sos=signal.butter(4,ny,btype='low',output='sos'); r=signal.sosfilt(sos,a).astype(np.float32)
    pk=signal.iirpeak(cut,res); ps=signal.lfilter(pk[0],pk[1],a).astype(np.float32)
    return norm(r+ps*0.15)

def fx_hp(a, cut=200):
    ny=cut/(SR/2); ny=max(0.01,min(0.99,ny))
    return signal.sosfilt(signal.butter(4,ny,btype='high',output='sos'),a).astype(np.float32)

def fx_formant(a, vowel='a'):
    fm={'a':[(800,10),(1150,8),(2900,6)],'e':[(400,10),(1600,8),(2700,6)],
        'i':[(350,10),(2300,8),(3200,6)],'o':[(450,10),(800,8),(2830,6)],'u':[(325,10),(700,8),(2530,6)]}
    r=np.zeros_like(a)
    for f,q in fm.get(vowel,fm['a']):
        b,aa=signal.iirpeak(f,q,fs=SR); r+=signal.lfilter(b,aa,a).astype(np.float32)
    return norm(r)

# ── VOICE CHOP ──
def chop(a, n=8, gate=0.5):
    sl=len(a)//n; slices=[]
    for i in range(n):
        s=a[i*sl:(i+1)*sl].copy(); env=np.abs(s); th=np.max(env)*(1-gate)
        ab=np.where(env>th)[0]
        if len(ab)>0: s=s[ab[0]:ab[-1]+1]
        slices.append(fad(s))
    return slices

def rearrange(sl, pat=None):
    if pat is None: pat=[0,2,1,3,0,3,2,1]
    r=np.zeros(0,dtype=np.float32)
    for i in pat:
        if i<len(sl): r=np.concatenate([r,sl[i]])
    return r

# ── PATTERNS ──
def bpms(bpm, sub='16th'):
    bps=bpm/60; subs={'whole':1,'half':2,'quarter':4,'8th':8,'16th':16,'32nd':32,'64th':64}
    return int(SR/(bps*subs.get(sub,16)/4))

PRESETS = {
    "breakcore_170": {"bpm":170,
        "kick":[1,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0,1,0,0,0,1,0,0,1,0,1,1,0,0,0,1,0],
        "snare":[0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,0,1,0,1,0,0,0,1,1,0,1],
        "hat":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        "clap":[0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0]},
    "dubstep_140": {"bpm":140,
        "kick":[1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
        "snare":[0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
        "hat":[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],
        "open_hat":[0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1]},
    "phonk_130": {"bpm":130,
        "kick":[1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
        "snare":[0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1],
        "hat":[1,1,0,1,1,0,1,1,1,1,0,1,1,0,1,0],
        "clap":[0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0]},
    "amen_break": {"bpm":170,
        "kick":[1,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0],
        "snare":[0,0,1,0,1,0,0,1,0,0,1,0,0,1,0,0],
        "hat":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        "open_hat":[0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1]},
    "404_architecture": {"bpm":200,
        "kick":[1,0,0,1,0,1,0,0,1,0,1,0,0,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,1,0,0,0],
        "snare":[0,0,1,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,1,1,0,0,0,0,1,0,1,0,0,1,0,1],
        "hat":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        "rim":[0,1,0,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,1,0],
        "clap":[0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1]},
}

SOUNDS = {'kick':synth_kick,'snare':synth_snare,'hat':synth_hat,
          'open_hat':lambda: synth_hat(open=True),'clap':synth_clap,'rim':synth_rim}
BASS = {'sub':synth_sub,'reese':synth_reese,'wobble':synth_wobble,'phonk':synth_phonk_bass,'scream':synth_scream}
FX = {'distortion':fx_dist,'bitcrush':fx_crush,'reverb':fx_reverb,'delay':fx_delay,'lowpass':fx_lp,'highpass':fx_hp,'formant':fx_formant}

def render_pattern(pat, bpm=170, bars=2):
    sl=bpms(bpm); ts=16*bars; total=sl*ts; r=np.zeros(total,dtype=np.float32)
    snds={k:fn() for k,fn in SOUNDS.items()}
    for v,steps in pat.items():
        if v not in snds: continue
        s=snds[v]
        for i,vel in enumerate(steps):
            if vel>0 and i<ts:
                st=i*sl; e=min(st+len(s),total); r[st:e]+=s[:e-st]*vel
    return norm(r)

def render_track(preset="breakcore_170", bars=4, bass="wobble", bf=55, fx_chain=None, bpm_override=None):
    p=PRESETS.get(preset,PRESETS["breakcore_170"]); bpm=bpm_override or p["bpm"]
    drums=render_pattern(p,bpm,bars)
    bd=60.0/bpm*bars*4; bass_fn=BASS.get(bass,synth_sub)
    bass_audio=bass_fn(bd,bf) if bass!='sub' else bass_fn(bd,bf)
    total=max(len(drums),len(bass_audio))
    dp=np.zeros(total,dtype=np.float32); bp=np.zeros(total,dtype=np.float32)
    dp[:len(drums)]=drums; bp[:len(bass_audio)]=bass_audio
    mix=dp*0.7+bp*0.5; mix=norm(mix)
    if fx_chain:
        for f in fx_chain:
            fn=FX.get(f["name"])
            if fn: mix=fn(mix,**f.get("params",{}))
    return fad(mix,0.01,0.05)

def gen_drumkit(name="evez_breakcore", style="breakcore"):
    kd=BASE_DIR/"drumkits"/name; kd.mkdir(parents=True,exist_ok=True); files={}
    for i,(f,d) in enumerate([(55,8),(45,6),(60,12),(35,5)]):
        p=kd/f"kick_{i+1}.wav"; sf.write(str(p),synth_kick(freq=f,dec=d),SR); files[f"kick_{i+1}"]=str(p)
    for i,(f,nm) in enumerate([(200,0.7),(180,0.8),(250,0.6),(160,0.9)]):
        p=kd/f"snare_{i+1}.wav"; sf.write(str(p),synth_snare(freq=f,nm=nm),SR); files[f"snare_{i+1}"]=str(p)
    for fn,oh in [("hat_closed_1",False),("hat_closed_2",False),("hat_open_1",True),("hat_open_2",True)]:
        p=kd/f"{fn}.wav"; sf.write(str(p),synth_hat(open=oh),SR); files[fn]=str(p)
    for i in range(3):
        p=kd/f"clap_{i+1}.wav"; sf.write(str(p),synth_clap(layers=3+i*2),SR); files[f"clap_{i+1}"]=str(p)
    p=kd/"rimshot.wav"; sf.write(str(p),synth_rim(),SR); files["rimshot"]=str(p)
    if style in("breakcore","404"):
        for i in range(3):
            k=fx_dist(synth_kick(freq=50+i*10,dec=10),drive=4+i*2)
            p=kd/f"kick_distorted_{i+1}.wav"; sf.write(str(p),k,SR); files[f"kick_distorted_{i+1}"]=str(p)
    m={"name":name,"style":style,"samples":len(files),"files":files}
    (kd/"manifest.json").write_text(json.dumps(m,indent=2)); return m

# ── HTTP ──
class H(BaseHTTPRequestHandler):
    def log_message(self,*a): pass
    def j(self,d,s=200):
        self.send_response(s); self.send_header("Content-Type","application/json")
        self.send_header("Access-Control-Allow-Origin","*"); self.end_headers()
        self.wfile.write(json.dumps(d,indent=2).encode())
    def do_GET(self):
        p=self.path.split("?")[0]
        if p=="/api/health": self.j({"status":"READY","presets":list(PRESETS.keys()),"bass":list(BASS.keys()),"fx":list(FX.keys())})
        elif p=="/api/presets": self.j({k:{"bpm":v["bpm"],"voices":list(v.keys())} for k,v in PRESETS.items()})
        elif p=="/": self.j({"service":"EVEZ DAW","presets":list(PRESETS.keys()),"bass_types":list(BASS.keys()),"fx":list(FX.keys()),"endpoints":["/api/render","/api/drumkit","/api/chop","/api/presets"]})
        else: self.j({"error":"not found"},404)
    def do_POST(self):
        p=self.path.split("?")[0]; l=int(self.headers.get("Content-Length",0))
        b=json.loads(self.rfile.read(l)) if l>0 else {}
        if p=="/api/render":
            audio=render_track(b.get("preset","breakcore_170"),b.get("bars",4),
                b.get("bass","wobble"),b.get("bass_freq",55),b.get("fx_chain"),b.get("bpm"))
            fn=b.get("filename",f"evez_{b.get('preset','track')}_{int(time.time())}.wav")
            path=BASE_DIR/"output"/fn; path.parent.mkdir(parents=True,exist_ok=True)
            sf.write(str(path),audio,SR)
            self.j({"filename":fn,"path":str(path),"duration":len(audio)/SR,"bpm":b.get("bpm",PRESETS.get(b.get("preset","breakcore_170"),{}).get("bpm",170))})
        elif p=="/api/drumkit":
            m=gen_drumkit(b.get("name","evez_breakcore"),b.get("style","breakcore"))
            self.j(m)
        elif p=="/api/chop":
            sp=b.get("sample_path","")
            if sp and os.path.exists(sp):
                a,sr=sf.read(sp); sl=chop(a.astype(np.float32),b.get("slices",8),b.get("gate",0.5))
                pat=b.get("rearrange"); r=rearrange(sl,pat) if pat else np.concatenate(sl)
                fn=b.get("filename",f"chopped_{int(time.time())}.wav")
                path=BASE_DIR/"output"/fn; sf.write(str(path),r,SR)
                self.j({"filename":fn,"path":str(path),"slices":len(sl)})
            else: self.j({"error":"sample not found"},400)
        else: self.j({"error":"not found"},404)

if __name__=="__main__":
    import argparse; pa=argparse.ArgumentParser()
    pa.add_argument("--port",type=int,default=9112); a=pa.parse_args()
    gen_drumkit()
    s=HTTPServer(("0.0.0.0",a.port),H)
    print(f"EVEZ DAW on :{a.port}"); s.serve_forever()
