---
name: coding-plan-assistant
description: "coding-plan-assistant"
---

# coding-plan-assistant

绠＄悊鍚勭缂栫▼鍔╂墜锛圕oding Plan锛夌殑娉ㄥ唽銆佽喘涔板拰鍑嵁閰嶇疆娴佺▼銆?
## 鍔熻兘姒傝堪

鏈妧鑳芥彁渚涗互涓嬪姛鑳斤細
- 馃搵 **骞冲彴娓呭崟**锛氭敮鎸佷富娴?AI 缂栫▼鍔╂墜骞冲彴
- 馃敆 **娉ㄥ唽寮曞**锛氭彁渚涘悇骞冲彴鐨勬敞鍐?璐拱閾炬帴鍜屾楠ゆ寚鍗?- 馃攼 **鍑嵁绠＄悊**锛氬畨鍏ㄥ瓨鍌ㄥ拰绠＄悊 API Key锛堝瓨鍌ㄥ湪 `.openclaw/.env`锛?- 馃挵 **鎴愭湰瀵规瘮**锛氭彁渚涘悇骞冲彴鐨勫畾浠峰姣斿拰鎺ㄨ崘鏂规
- 鉁?**鐘舵€佹娴?*锛氳嚜鍔ㄦ娴嬪凡閰嶇疆鐨勫嚟鎹姸鎬?
## 鏀寔鐨勫钩鍙?
| 骞冲彴 | 绫诲瀷 | 鍏嶈垂棰濆害 | 浠樿垂璧风偣 |
|------|------|----------|----------|
| GitHub Copilot | 浠ｇ爜琛ュ叏/鑱婂ぉ | 瀛︾敓鍏嶈垂 | $10/鏈?|
| Claude Code | CLI 缂栫▼鍔╂墜 | 鏈夐檺鍏嶈垂 | $20/鏈?|
| Gemini CLI | Google 缂栫▼鍔╂墜 | 鏈夐檺鍏嶈垂 | $20/鏈?|
| Codex (OpenAI) | API 璁块棶 | 鏂扮敤鎴疯禒閲?| 鎸夐噺浠樿垂 |
| 闃块噷浜戠櫨鐐?Qwen Code | 闃块噷浜戠紪绋嬪姪鎵?| 鏈夐檺鍏嶈垂 | 鎸夐噺浠樿垂 |
| 鐧惧害椋炴〃 | 鐧惧害 AI 骞冲彴 | 鏈夐檺鍏嶈垂 | 鎸夐噺浠樿垂 |
| OpenRouter | 澶氭ā鍨嬭仛鍚?| 鏈夊厤璐规ā鍨?| 鎸夐噺浠樿垂 |

## 浣跨敤鏂瑰紡

### 鍩烘湰鍛戒护

瀵?智能体 璇达細
- "甯垜娉ㄥ唽 Claude Code"
- "鏌ョ湅宸查厤缃殑缂栫▼鍔╂墜"
- "瀵规瘮鍚勫钩鍙扮殑浠锋牸"
- "閰嶇疆 GitHub Copilot"
- "杞崲 OpenAI API Key"

### 鑷劧璇█鏌ヨ绀轰緥

```
"鎴戞兂鐢?Claude Code锛屾€庝箞娉ㄥ唽锛?
"鍝釜缂栫▼鍔╂墜鏈€渚垮疁锛?
"甯垜妫€鏌?API Key 閰嶇疆鐘舵€?
"濡備綍鏇存崲鎴戠殑 API Key锛?
"鎺ㄨ崘涓€涓€傚悎瀛︾敓鐨勭紪绋嬪姪鎵?
```

## 瀹夊叏瑕佹眰

### 鍑嵁瀛樺偍
- 鉁?鎵€鏈?API Key 瀛樺偍鍦?`.openclaw/.env`锛堝伐浣滅┖闂存牴鐩綍锛?- 鉁?璇ユ枃浠跺凡鍔犲叆 `.gitignore`锛屼笉浼氭彁浜ゅ埌 Git
- 鉁?涓嶅湪鏃ュ織鎴栬緭鍑轰腑鏄庢枃鏄剧ず瀹屾暣 Key

### 鍑嵁鏍煎紡
```env
# .openclaw/.env
GITHUB_COPILOT_TOKEN=ghp_xxxx...xxxx
CLAUDE_API_KEY=sk-ant-xxxx...xxxx
OPENAI_API_KEY=sk-xxxx...xxxx
GEMINI_API_KEY=xxxx...xxxx
QWEN_API_KEY=xxxx...xxxx
BAIDU_API_KEY=xxxx...xxxx
OPENROUTER_API_KEY=sk-or-xxxx...xxxx
```

### 鑴辨晱鏄剧ず
鎵€鏈?API Key 鍦ㄨ緭鍑烘椂鑷姩鑴辨晱锛?- `sk-xxxx...xxxx` 鈫?`sk-xxxx...***`
- `ghp_xxxx...xxxx` 鈫?`ghp_...***`

## 閰嶇疆璇存槑

### 棣栨浣跨敤

1. **鏌ョ湅鎶€鑳界姸鎬?*
   ```
   妫€鏌ョ紪绋嬪姪鎵嬮厤缃?   ```

2. **閰嶇疆 API Key**
   ```
   閰嶇疆 OpenAI API Key
   ```
   鎶€鑳戒細寮曞浣犲畨鍏ㄨ緭鍏ュ嚟鎹€?
3. **楠岃瘉閰嶇疆**
   ```
   楠岃瘉 API Key
   ```

### 閰嶇疆鏂囦欢

**config.json**锛堟妧鑳界洰褰曪級
```json
{
  "platforms": {
    "github-copilot": {
      "name": "GitHub Copilot",
      "envKey": "GITHUB_COPILOT_TOKEN",
      "registerUrl": "https://github.com/features/copilot",
      "pricingUrl": "https://github.com/features/copilot#pricing"
    }
    // ... 鍏朵粬骞冲彴
  }
}
```

## 鑴氭湰宸ュ叿

### scripts/check-status.js
妫€鏌ユ墍鏈夊钩鍙扮殑鍑嵁閰嶇疆鐘舵€併€?
```bash
node scripts/check-status.js
```

### scripts/rotate-key.js
杞崲鎸囧畾骞冲彴鐨?API Key銆?
```bash
node scripts/rotate-key.js <platform>
```

### scripts/compare-pricing.js
瀵规瘮鍚勫钩鍙扮殑瀹氫环鏂规銆?
```bash
node scripts/compare-pricing.js
```

## 瀹樻柟鏂囨。閾炬帴

璇﹁ `references/` 鐩綍锛?- `github-copilot.md`
- `claude-code.md`
- `gemini-cli.md`
- `codex-openai.md`
- `qwen-code.md`
- `baidu-paddle.md`
- `openrouter.md`

## 鏁呴殰鎺掓煡

### 甯歌闂

**Q: API Key 鏃犳晥锛?*
A: 妫€鏌?Key 鏄惁姝ｇ‘澶嶅埗锛岀‘璁よ处鎴锋湁鍙敤棰濆害銆?
**Q: 濡備綍鏌ョ湅宸查厤缃殑 Key锛?*
A: 杩愯 `妫€鏌ョ紪绋嬪姪鎵嬮厤缃甡锛孠ey 浼氳劚鏁忔樉绀恒€?
**Q: 鍑嵁鏂囦欢鍦ㄥ摢閲岋紵**
A: `.openclaw/.env`锛堝伐浣滅┖闂存牴鐩綍锛?
### 瀹夊叏鎻愰啋

- 鈿狅笍 涓嶈灏?`.env` 鏂囦欢鍒嗕韩缁欎粬浜?- 鈿狅笍 涓嶈灏?API Key 鎻愪氦鍒?Git
- 鈿狅笍 瀹氭湡杞崲鏁忔劅鍑嵁
- 鈿狅笍 鎬€鐤戞硠闇叉椂绔嬪嵆杞崲 Key

## 鐗堟湰鍘嗗彶

- **1.0.0** (2026-03-27): 鍒濆鐗堟湰
  - 鏀寔 7 涓富娴佺紪绋嬪姪鎵嬪钩鍙?  - 瀹炵幇鍑嵁瀹夊叏绠＄悊
  - 鎻愪緵娉ㄥ唽寮曞鍜屾垚鏈姣?
## 寮€鍙戣€呰鏄?
### 娣诲姞鏂板钩鍙?
1. 鍦?`config.json` 涓坊鍔犲钩鍙伴厤缃?2. 鍦?`references/` 涓垱寤哄畼鏂规枃妗ｉ摼鎺?3. 鏇存柊 `SKILL.md` 鐨勫钩鍙版竻鍗?
### 鐩綍缁撴瀯

```
coding-plan-assistant/
鈹溾攢鈹€ SKILL.md           # 鎶€鑳借鏄庯紙鏈枃浠讹級
鈹溾攢鈹€ index.js           # 涓荤▼搴忓叆鍙?鈹溾攢鈹€ config.json        # 骞冲彴閰嶇疆
鈹溾攢鈹€ package.json       # NPM 閰嶇疆
鈹溾攢鈹€ scripts/           # 杈呭姪鑴氭湰
鈹?  鈹溾攢鈹€ check-status.js
鈹?  鈹溾攢鈹€ rotate-key.js
鈹?  鈹斺攢鈹€ compare-pricing.js
鈹斺攢鈹€ references/        # 瀹樻柟鏂囨。閾炬帴
    鈹溾攢鈹€ github-copilot.md
    鈹溾攢鈹€ claude-code.md
    鈹溾攢鈹€ gemini-cli.md
    鈹溾攢鈹€ codex-openai.md
    鈹溾攢鈹€ qwen-code.md
    鈹溾攢鈹€ baidu-paddle.md
    鈹斺攢鈹€ openrouter.md
```

