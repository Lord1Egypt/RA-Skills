---
name: bank-scan-household-splitter
slug: bank-scan-household-splitter
displayName: 银行扫描件按户拆分·身份证正反面自动归户成Word
description: >-
  客户丢来一个压缩包，里面几百张身份证正反面、开卡申请书、合同——**人工一张张挑，一下午就没了，还容易漏**。

  这套按人按户自动拆好：解包 → 抽出全部图片 → 视觉模型批量识别"这是谁的正/反面、哪份申请书" → 按户匹配 → 每户输出一个独立 Word。

  有一条用真金白银换来的选型红线：**证件识别不要用 GLM-4V-Flash**（实测 18 张身份证背面里 11 张被编造，还编出了姓名），必须用高准确度视觉模型并配交叉校验。

  - 输入：RAR/ZIP 加密压缩包，或几百页全是图片、没有文字的扫描件 docx
  - 输出：「姓名-身份证+开申请书.docx」单户文件 + 「待人工核对」文件夹（识别不出或匹配不上的单独放，不混进正常结果）
  - 图片不出本机：解包与提取都在本地做，只有识别那一步调视觉模型

  适用：银行影像材料归户、律师立案材料整理、催收/诉讼材料分户、批量证件归档。

  触发词：扫描件拆分、材料按户分开、银行影像材料、身份证正反面识别、归户、批量证件归档、律所立案材料、docx 提取图片、OCR 分类、催收材料整理。
  适用对象：银行影像材料归户、律师立案材料整理、催收/诉讼材料分户、批量证件归档。
  输入：RAR/ZIP 加密压缩包，或几百页的扫描件 docx（全是图片、无文字）
  输出：「姓名-身份证+开申请书.docx」单户文件 + 「待人工核对」文件夹（识别不出/匹配不上的单独放，不混进正常结果）

  核心做法：解包 → 从 docx 抽出 word/media 全部图片 → 视觉模型批量识别「这是谁的正/反面、哪份申请书」→ 按户匹配 → 生成单户 Word。
  ⚠️ 里面有一条用真金白银换来的选型红线：证件识别**不要用 GLM-4V-Flash**（实测 18 张身份证背面里 11 张被编造，还编出姓名），必须用豆包 Seed 2.0 Pro 这类高准确度视觉模型，并配交叉校验。

  触发词：扫描件拆分、材料按户分开、银行影像材料、身份证正反面识别、归户、批量证件归档、律所立案材料、docx 提取图片、OCR 分类。
  图片不出本机（解包与提取全在本地做），只有识别那一步调视觉模型。
version: 1.1.0
author: 九品锦锂e
summary: 一堆扫描件按人/户自动拆分归档，每户输出独立Word（身份证正反面+申请书一张不漏），识别不出单独放不混进结果。
license: MIT
metadata:
  version: "1.1.0"
category: office-efficiency

---
# 银行材料扫描件按户拆分（批量材料→单户Word）

## 触发条件
- 客户（律所/银行/催收机构）发来批量材料压缩包（RAR/ZIP 加密）或大 docx（61MB+，全是扫描件图片）
- 要求"把身份证和开卡申请书拆出来，分别放到各自的 Word 文件里"
- 要求"单户 Word = 该客户身份证正面 + 对应背面 + 对应银行申请材料，一个不能漏"
- 用户强调"从头检查一遍"——此类任务质量要求高，识别错误=客户损失

## 用户铁律（2026-08-19 用户）
1. **单户 Word 必须包含**：身份证正面 + 对应背面（国徽页）+ 对应申请材料（申请书），一张不漏
2. **文件名标注清楚**：`姓名-身份证+开卡申请书.docx`
3. **待人工核对**：识别不出/无法匹配的单独放"待人工核对"文件夹，不混在正常结果里
4. 用户要求统计：从识别开始到完成分拆的**耗时、调用次数、token、费用**——客户可复用定价依据

## 完整工作流（5步）

### Step1 解包
```bash
# 加密RAR用7z（本机 C:\Program Files\7-Zip\7z.exe）
"C:/Program Files/7-Zip/7z.exe" x -p"密码" input.rar -y
# 客户给的密码要问用户；RAR5格式7z可解
```
- 常见形态：RAR解压后是**一个超大 docx**（如《影像材料2.docx》61MB），里面没有文字，全是图片

### Step2 从docx提取图片
```python
import zipfile
with zipfile.ZipFile('影像材料2.docx') as z:
    media = [f for f in z.namelist() if f.startswith('word/media/') and f.endswith('.png')]
    for f in media: z.extract(f, out_dir)
```
- docx本质是zip，图片在 word/media/ 下，命名 image1.png~imageN.png
- **图片编号 = 原始扫描顺序**，后面归户会用到

### Step3 视觉识别分类（⭐核心：模型选型）
**绝不用 GLM-4V-Flash 做关键证件识别！**（本session实测幻觉：11/18张身份证背面被编造成"正面"+编造姓名）

用**豆包 Seed 2.0 Pro**（`doubao-seed-2-0-pro-260215`，VLM，准确）：
```python
payload = {
    "model": "doubao-seed-2-0-pro-260215",
    "messages": [{"role": "user", "content": [
        {"type": "text", "text": "这是银行客户材料扫描件。判断类别并提取关键信息：\n类别只能是：身份证正面、身份证背面、开卡申请书、信用卡申请书、其他材料\n正面→提取姓名+身份证号；背面→提取签发机关；申请书→提取申请人姓名\n输出格式：类别：XXX\n姓名：XXX（无则写无）\n身份证号：XXX\n签发机关：XXX"},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
    ]}],
    "max_tokens": 200
}
# base_url: https://ark.cn-beijing.volces.com/api/v3/chat/completions
# KEY: .env 的 ARK_API_KEY
```
- 每张间隔1s防限流，每15张存进度json（断点续传），重试3次（429/超时等5-8s）
- 136张约35-40分钟（17s/张）——**后台跑+notify_on_complete**

### Step4 按户归组（正面定户→背面匹配→申请书匹配）
1. **正面姓名定户**：每张"身份证正面"提取姓名→建户（每户有fronts/backs/apps三个列表）
2. **背面匹配**（按签发机关地区 ↔ 正面身份证前6位地区码）：
   - 维护地区码→公安局名映射表（450122=武鸣、452128=武鸣、450126=宾阳...广西为主，客户是广西银行时）
   - 匹配成功→归户；**市级签发机关（南宁市公安局/柳州市公安局）无法唯一匹配**→豆包成对对比（一次传正面+背面两张图问"是否同一人"）或待人工核对
3. **申请书匹配**（姓名）：直接匹配 + **拼音模糊匹配**（pypinyin）：
   - `lazy_pinyin(name)` 前2字同音即匹配（黄祉玲→黄令、唐咸梅→唐凤梅、姚贤明→姚先明）
   - 手写体申请书姓名识别偏差大，模糊匹配是救回的关键
4. **⚠️ 别用"原始顺序相邻"匹配正反面**——多人混排时会把别人背面归错户（本session教训：顺序匹配44张>实际34张）

### Step5 生成单户Word（python-docx）
```python
from docx import Document
from docx.shared import Cm
doc = Document()
# 标题（居中加粗）：{姓名} - 银行材料
# 【身份证正面】→ 图宽8cm，逐张 add_picture + 空行
# 【身份证背面】→ 同上
# 【银行申请材料】→ 图宽12cm
doc.save(f"{out_dir}/{name}-身份证+开卡申请书.docx")
```
- 文件名：`{姓名}-身份证+开卡申请书.docx`
- 未匹配背面/申请书 → 复制到 `待人工核对/` 子目录

## 成本统计（用户要求，交付时给）
```python
# 从API响应 usage 字段累计：prompt_tokens/completion_tokens
# 估算：高清扫描件每张≈2000 tokens输入、200 tokens输出
# 豆包Seed 2.0 Pro视觉：输入≈0.008元/千tokens → 136张全量约2-5元
# 耗时：从识别开始到Word完成
```
交付给用户的统计表：调用次数、输入/输出tokens、估算费用、总耗时（本session：136张≈180次调用、45万tokens、3-5元、35分钟识别+几分钟归户）

## 关键坑
1. **GLM-4V-Flash幻觉**（本session最痛教训）：识别不出就"编"——把背面编成正面+编造姓名。关键识别必须用豆包
2. **docx图片提取**：用zipfile直接读 word/media/，不要用python-docx的inline_shapes（大文件慢且不全）
3. **PIL图像增强**：RGBA模式要先 convert('RGB') 才能做 Contrast/Sharpness/autocontrast；旋转90°的身份证 h>w*1.5 时生成 ±90°两个版本分别识别
4. **地区码映射表**：广西为主时手工维护县→公安局映射（4501=南宁、4502=柳州...），客户是外省时按身份证前6位查行政区划
5. **豆包慢**：17s/张，批量必须后台跑+断点续传，别前台等
6. 识别"看不清"的件：先PIL增强再二次识别，仍不行才进待人工核对

## 相关技能
- 视觉模型矩阵/费用纪律：见 model-cost-discipline（user-owned，仅参考）
- 本地OCR：deepseek-ocr（Ollama）适合整页文字OCR，不适合证件分类

---

## 关于作者

**九品锦锂e** ｜ 把踩过的坑封装成「拿来就能跑」的 skill，不写教科书。

这个 skill 是我自己在用的版本，里面每条坑都是真踩过的。**用的时候卡住了、想要进阶玩法、或者有别的场景想让我封装成 skill**，直接加我微信说，加时备注「SkillHub」我优先通过：

![九品锦锂e 微信二维码](https://jinli-vault-1372591613.cos.ap-guangzhou.myqcloud.com/skillhub/hook-wechat-jiupinjinlie.png)

> 扫码添加作者微信 · 备注「SkillHub」优先通过
