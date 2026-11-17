# -*- coding: utf-8 -*-
"""
豆包 Seed 2.0 Pro 批量识别扫描件（断点续传+重试+usage累计）
用法：python doubao_batch_classify.py <图片目录> <输出json路径>
每张输出：类别/姓名/身份证号/签发机关
"""
import sys, os, json, base64, urllib.request, time, glob, re

def get_env_key(var_name, env_path=None):
    """优先读环境变量；没有则依次找常见 .env 位置（不写死任何机器路径）"""
    if os.environ.get(var_name):
        return os.environ[var_name]
    cands = [env_path] if env_path else []
    cands += [os.path.expanduser("~/.env"),
              os.path.join(os.path.expanduser("~"), ".config", ".env"),
              os.path.join(os.getcwd(), ".env")]
    for p in cands:
        if p and os.path.exists(p):
            with open(p, encoding='utf-8', errors='replace') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(var_name + '='):
                        return line.split('=', 1)[1]
    return ''

KEY = get_env_key('ARK_API_KEY')
URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
MODEL = "doubao-seed-2-0-pro-260215"

PROMPT = ("这是银行客户材料扫描件。判断类别并提取关键信息：\n"
          "类别只能是以下之一：身份证正面、身份证背面、开卡申请书、信用卡申请书、其他材料\n"
          "如果正面：提取姓名和身份证号\n"
          "如果背面：提取签发机关\n"
          "如果申请书：提取申请人姓名\n"
          "输出格式：\n类别：XXX\n姓名：XXX（无则写无）\n身份证号：XXX（无则写无）\n签发机关：XXX（无则写无）")

def classify_one(path):
    """返回 (内容, prompt_tokens, completion_tokens)"""
    with open(path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": PROMPT},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
        ]}],
        "max_tokens": 200
    }
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                d = json.loads(resp.read().decode())
            usage = d.get('usage', {})
            return (d["choices"][0]["message"]["content"],
                    usage.get('prompt_tokens', 0), usage.get('completion_tokens', 0))
        except Exception as e:
            if '429' in str(e) or 'Too Many' in str(e):
                time.sleep(8); continue
            if 'timeout' in str(e).lower() or 'timed out' in str(e).lower():
                time.sleep(5); continue
            return (f"[错误:{str(e)[:60]}]", 0, 0)
    return ("[重试失败]", 0, 0)

def main(img_dir, out_path, resume_every=15):
    files = sorted(glob.glob(os.path.join(img_dir, 'image*.png')))
    results = {}
    # 断点续传：加载已有进度
    if os.path.exists(out_path):
        with open(out_path, encoding='utf-8') as f:
            results = json.load(f)
    done = set(results.keys())
    pending = [f for f in files if os.path.basename(f) not in done]

    total_prompt = total_completion = 0
    t0 = time.time()
    for i, f in enumerate(pending):
        name = os.path.basename(f)
        content, pt, ct = classify_one(f)
        results[name] = content
        total_prompt += pt; total_completion += ct
        print(f"[{i+1}/{len(pending)}] {name}: {content[:60]}")
        time.sleep(1)
        if (i + 1) % resume_every == 0:
            with open(out_path, 'w', encoding='utf-8') as fp:
                json.dump(results, fp, ensure_ascii=False, indent=2)

    with open(out_path, 'w', encoding='utf-8') as fp:
        json.dump(results, fp, ensure_ascii=False, indent=2)
    print(f"\n完成 {len(results)}张, 耗时{time.time()-t0:.0f}s")
    print(f"usage: prompt={total_prompt}, completion={total_completion}")
    print(f"估算费用: {total_prompt/1000*0.008 + total_completion/1000*0.002:.2f}元")

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
