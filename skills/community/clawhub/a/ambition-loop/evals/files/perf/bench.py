import json, random, time, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from dedupe import dedupe
random.seed(1)
N = int(os.environ.get("N", "20000"))
events = [{"user": random.randint(1, 3000), "type": random.choice(["view", "click", "buy"]), "ts": random.randint(0, 500)} for _ in range(N)]
t = time.perf_counter(); r = dedupe(events); dt = time.perf_counter() - t
print(json.dumps({"n": N, "unique": len(r), "seconds": round(dt, 4)}))
