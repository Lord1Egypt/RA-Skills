"""单模型基准测试: 定位哪个模型/解码配置能在本机内存下跑通, 并给出耗时

用法: python -u scripts/bench_transcribe.py <model> <beam> <wav> [threads]
"""
import os, sys, time

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HUB_DISABLE_XET"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"

from faster_whisper import WhisperModel

name = sys.argv[1]
beam = int(sys.argv[2])
wav = sys.argv[3]
threads = int(sys.argv[4]) if len(sys.argv) > 4 else 1
PROMPT = "以下是普通话的句子，请使用简体中文输出。"


def mem():
    import ctypes

    class MS(ctypes.Structure):
        _fields_ = [('dwLength', ctypes.c_ulong), ('dwMemoryLoad', ctypes.c_ulong),
                    ('ullTotalPhys', ctypes.c_ulonglong), ('ullAvailPhys', ctypes.c_ulonglong),
                    ('ullTotalPageFile', ctypes.c_ulonglong), ('ullAvailPageFile', ctypes.c_ulonglong),
                    ('ullTotalVirtual', ctypes.c_ulonglong), ('ullAvailVirtual', ctypes.c_ulonglong),
                    ('ullAvailExtendedVirtual', ctypes.c_ulonglong)]
    m = MS(); m.dwLength = ctypes.sizeof(MS)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.ullAvailPhys / 2 ** 30, m.ullAvailPageFile / 2 ** 30


print(f"start model={name} beam={beam} threads={threads} | freeRAM={mem()[0]:.2f}GB", flush=True)
t0 = time.time()
try:
    m = WhisperModel(name, device="cpu", compute_type="int8", cpu_threads=threads, num_workers=1)
except Exception as ex:
    print(f"LOAD FAILED {type(ex).__name__}: {str(ex)[:200]}", flush=True)
    sys.exit(2)
t1 = time.time()
print(f"loaded in {t1 - t0:.1f}s | freeRAM={mem()[0]:.2f}GB", flush=True)
try:
    segs, _ = m.transcribe(wav, language="zh", beam_size=beam, vad_filter=True,
                           initial_prompt=PROMPT, condition_on_previous_text=False)
    n, first = 0, []
    for sg in segs:
        if n < 6:
            first.append(f"{sg.start:6.1f} {sg.text}")
        n += 1
        if n % 10 == 0:
            print(f"  ... {n} segs, t={time.time() - t1:.0f}s", flush=True)
    print("FIRST SEGMENTS:")
    for f in first:
        print("   ", f, flush=True)
    print(f"RESULT ok model={name} beam={beam} segs={n} time={time.time() - t1:.1f}s", flush=True)
except Exception as ex:
    print(f"TRANSCRIBE FAILED {type(ex).__name__}: {str(ex)[:200]}", flush=True)
    sys.exit(3)
