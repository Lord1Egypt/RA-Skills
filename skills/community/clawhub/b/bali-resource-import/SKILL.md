---
name: bali-resource-import
description: |
  印尼（巴厘岛）旅游资源入库 SOP。当用户提供供应商文档（PDF/Word）并要求解析入库时，
  或提到"资源入库"、"解析入库"、"印尼资源"、"巴厘岛资源"、"CSV入库"时，必须使用本技能。
  覆盖8类资源：酒店、车辆、景点、活动、SPA、俱乐部、餐厅、下午茶。
  使用前必须先检索同类资源 CSV 的表头格式（encoding 可能是 gbk 或 utf-8-sig），
  确保新增数据字段与生产库表头完全一致后再写入。
compatibility: Python 3.8+, PyMuPDF（PDF解析）, python-docx（Word解析）；csv 内置，redis 可选
---

# 印尼旅游资源解析入库技能

## 触发识别（使用前必读）

### 用户提示词关键词解析

收到入库任务时，从用户提示词中自动识别以下关键信息：

| 提示词关键词 | 识别结果 | 操作 |
|------------|---------|------|
| `https://drive.google.com/...` 等 Drive URL | 数据源为云盘 | 调用 `google-drive` 技能，**只下载合同文件**到目标路径 |
| 本地路径如 `C:\Users\a\Desktop\资源` | 数据源为本地文件 | 直接使用该路径下的文件 |
| `模型文件路径` / `已存在的 csv` | 目标生产库位置 | 在该 CSV 基础上**追加**新数据，而非覆盖 |
| `目标路径` / `target` | 解析结果输出目录 | 解析结果写入该目录，原始合同和中间文件于 Step 8 清理 |
| 未提及目标路径 | — | 告知用户必须指定目标路径 |

**⚠️ 路径仅为示例，不可硬编码。** 所有路径必须从用户提示词中动态提取，用作字段值传递给脚本。

**示例提示词：**
> "检索 https://drive.google.com/drive/my-drive 所有合同并解析，模型文件路径在 `C:\Users\a\Desktop\资源`，目标路径为 `C:\Users\a\Desktop\资源\target`"

**动态提取结果（作为变量使用）：**
- **数据源 URL**：`https://drive.google.com/drive/my-drive` → 传给 `google-drive` 技能
- **模型文件路径**：`C:\Users\a\Desktop\资源` → 拼接生产库 CSV 文件名，得到完整生产库路径
- **目标路径**：`C:\Users\a\Desktop\资源\target` → 解析结果输出目录

### 技能依赖检测

使用前检查所需技能是否已安装：

| 依赖技能 | 用途 | 未安装时操作 |
|---------|------|------------|
| `google-drive` | 访问 Google Drive 下载合同 | 提示用户执行 `openclaw skills install google-drive`，或告知用户提供本地文件 |
| `bali-resource-import` | 本技能（自身） | 提示用户提供正确路径 |
| `pdfplumber` / `PyMuPDF` | PDF 文本提取 | pip 安装 `pdfplumber` |

**缺失技能时的话术模板：**
```
[技能缺失] 解析入库需要先安装 google-drive 技能。
请在终端执行：openclaw skills install google-drive
安装完成后请重新发送任务。
```

## 使用流程

### Step 0：安装依赖

```bash
# 安装 Google Drive 技能（如需要）
openclaw skills install google-drive

# 安装 PDF 解析库
pip install pdfplumber
```

### Step 1：下载合同文件

**Google Drive 来源（仅下载合同文件）：**
1. 调用 `google-drive` 技能，传入 Drive URL，列出所有文件
2. **过滤合同文件**（非合同文件不下载）：
   - MIME 类型为 `application/pdf` 或 `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
   - 文件名包含合同相关关键词：`合同`、`Contract`、`contract`、`Agreement`、`agreement`、`协议`
   - 如无法判断，一律下载，由 Step 3 解析时判断资源类型
3. 下载匹配文件到**目标路径**
4. 返回下载文件列表供后续使用

**本地来源**：从提示词中提取本地路径，定位 PDF/Word 文件。

**⚠️ 所有路径均为动态变量，不写死。**

### Step 2：读取生产库表头

**⚠️ 必须先读取目标 CSV 的实际表头和 encoding，再生成数据行。**

```python
import csv

def read_production_csv(path):
    for enc in ['utf-8-sig', 'gbk', 'utf-8', 'latin1']:
        try:
            with open(path, 'r', encoding=enc) as f:
                headers = next(csv.reader(f))
            return headers, enc
        except UnicodeDecodeError:
            continue
    raise ValueError(f"无法读取 {path}")

# 示例
headers, enc = read_production_csv(r"C:\Users\a\Desktop\资源\活动标准化完整版_含人群标签与特色标签_V4.csv")
# headers = ['contract_id (合同编号)', 'activitynameen (活动英文名)', ...]
# ⚠️ 表头格式为 "fieldname (中文说明)"，提取时用 split(' (')[0] 取英文字段名
```

### Step 3：解析合同内容

按合同内容识别资源类型：

| 资源类型 | 判断关键词 | 核心价格字段 |
|---------|----------|------------|
| 酒店 | 房型、床型、早餐、入住、淡旺季 | 淡季价格_IDR / 旺季价格_IDR |
| 车辆 | 车型、半天、全天、司机、油费 | 半天价格 / 全天价格 |
| 景点 | 门票、开放时间、GPS、难度 | 门票-成人IDR |
| 活动 | 时长、含保险、含交通、教练语言 | 成人IDR价格 |
| SPA | 疗法、套餐、开放时间 | 成人IDR价格 |
| 俱乐部 | 最低消费、入场费、时段政策 | 入场/门票费用 |
| 餐厅 | 菜系、套餐、预约 | 成人IDR价格 |
| 下午茶 | 套餐类型、成人儿童价 | 成人IDR价格 |

### Step 4：数据提取规则

**提取原则（按优先级）：**

| 优先级 | 来源 | 处理方式 |
|--------|------|---------|
| 1 | 合同原文 | 直接使用，如实写入字段 |
| 2 | 公开网络信息（如 GPS 坐标） | 可填写，标注来源 |
| — | 合同无数据 | 填写"合同未提供"，不得留空 |
| — | 编造数据 | 严禁 |

**字段格式规范：**

| 字段类型 | 格式示例 |
|---------|---------|
| 日期期间 | `2024-07-01 至 2024-08-31`（不用英文月份） |
| 星级 | `5星`（带"星"字，非纯数字） |
| 价格 | 纯数字，不含货币符号（如 `3581500` 而非 `IDR 3,581,500`） |
| 汇率参考 | 1 CNY ≈ 2,100 IDR；1 USD ≈ 15,000 IDR |

### Step 5：三层标签体系

每条资源必须标注三层标签：

**人群标签（第一层）：** `#家庭 #亲子 #情侣 #商务 #蜜月 #年轻人 #老年人 #单身`

**风格标签（第二层）：** `#豪华 #经济型 #浪漫 #休闲 #刺激 #度假村风格 #自然 #文化`

**特色标签（第三层）：** 按资源类型选用，详见下方各资源标签表。

### Step 6：写入 CSV

**⚠️ 关键规则：**
1. 新增数据的字段名必须与生产库表头完全一致
2. encoding 必须与生产库一致（通常 activity 用 `gbk`，hotel 用 `utf-8-sig`）
3. 写入模式为**追加**（append），不覆盖原有数据

```python
import csv, os

def append_to_production(prod_path, data_rows, enc):
    """追加数据到生产库 CSV"""
    with open(prod_path, 'r', encoding=enc, newline='') as f:
        prod_rows = list(csv.reader(f))

    prod_headers = prod_rows[0]  # ['fieldname (中文说明)', ...]
    prod_fieldnames = [h.split(' (')[0] for h in prod_headers]  # ['fieldname', ...]

    with open(prod_path, 'w', encoding=enc, newline='') as f:
        writer = csv.writer(f)
        writer.writerow(prod_headers)          # 保留原有表头
        writer.writerows(prod_rows[1:])        # 保留原有数据
        for row in data_rows:                 # 追加新数据
            out_row = [row.get(fn, '') for fn in prod_fieldnames]
            writer.writerow(out_row)
```

**直接追加示例（不依赖 append_to_csv.py）：**
```python
# BOUNTY Cruises → 活动库
append_to_production(
    r"C:\Users\a\Desktop\资源\活动标准化完整版_含人群标签与特色标签_V4.csv",
    bounty_rows,  # list of dict
    'gbk'
)

# Maya Ubud → 酒店库
append_to_production(
    r"C:\Users\a\Desktop\资源\巴厘岛酒店资源库_2026标准版_V4_FINAL.csv",
    maya_rows,
    'utf-8-sig'
)
```

### Step 7：输出报告

入库完成后，**向用户报告（路径为实际从提示词中提取的值）**：

```
✅ 入库完成
━━━━━━━━━━━━━━━
合同文件：BOUNTY Cruises - March 2026.pdf / Maya Ubud Contract Valid 31 Mar 2025.pdf
资源类型：活动 × 4条 + 酒店 × 4条
目标库：
  活动库：{模型文件路径}\活动标准化完整版_含人群标签与特色标签_V4.csv → +4 条
  酒店库：{模型文件路径}\巴厘岛酒店资源库_2026标准版_V4_FINAL.csv → +4 条
输出目录：{目标路径}\
清理结果：原始合同 PDF + parsed_results.json 已删除
```

### Step 8：清理临时文件

**入库完成后，目标文件夹只保留结果 CSV 文件**，一律删除：

| 文件类型 | 示例 | 删除原因 |
|---------|------|---------|
| 原始合同 PDF/Word（云盘下载） | `BOUNTY Cruises - March 2026.pdf` | 原始合同不留在输出目录 |
| 解析中间文件 | `parsed_results.json` | 仅作中间处理使用，不交付用户 |
| 任何非结果 CSV 的残留文件 | `xxx_out.csv` 以外的临时文件 | 避免输出目录污染 |

**保留文件：**
```
{目标路径}\
├── BountyCruises活动数据_YYYYMMDD.csv   ← 新增的活动数据（追加到生产库）
└── MayaUbud酒店数据_YYYYMMDD.csv        ← 新增的酒店数据（追加到生产库）
```

```python
import os

def cleanup_target_dir(target_dir, keep_prefixes=('活动数据', '酒店数据', '景点数据', 'SPA数据', '餐厅数据', '俱乐部数据', '下午茶数据', '车费数据')):
    """清理目标目录，保留结果CSV，删除其余所有文件"""
    deleted = []
    for f in os.listdir(target_dir):
        full = os.path.join(target_dir, f)
        if os.path.isfile(full):
            # 保留带指定前缀的结果CSV
            if any(f.startswith(p) and f.endswith('.csv') for p in keep_prefixes):
                continue
            # 其余文件一律删除
            os.remove(full)
            deleted.append(f)
    return deleted

deleted = cleanup_target_dir(target_dir)
for f in deleted:
    print(f"[清理] 已删除: {f}")
```

## 8类资源 CSV 文件

| 资源类型 | CSV 文件名 | encoding |
|---------|-----------|---------|
| 酒店 | `巴厘岛酒店资源库_2026标准版_V4_FINAL.csv` | utf-8-sig |
| 车辆 | `巴厘岛车费成本表-成本_2.10.csv` | gbk |
| 景点 | `景点标准化完整版_含人群标签与特色标签_V4.csv` | gbk |
| 活动 | `活动标准化完整版_含人群标签与特色标签_V4.csv` | gbk |
| SPA | `SPA标准化完整版_含人群标签与特色标签_V4.csv` | gbk |
| 俱乐部 | `俱乐部标准化完整版_含人群标签与特色标签_V4.csv` | gbk |
| 餐厅 | `餐厅标准化完整版_含人群标签与特色标签_V4.csv` | gbk |
| 下午茶 | `下午茶标准化完整版_含人群标签与特色标签_V4.csv` | gbk |

## 三层标签参考

### 人群标签（所有资源）
`#家庭 #亲子 #情侣 #商务 #蜜月 #年轻人 #老年人 #单身`

### 风格标签（所有资源）
`#豪华 #经济型 #浪漫 #休闲 #刺激 #度假村风格 #自然 #文化`

### 特色标签（按资源类型）

**酒店：** `#海景房 #私人泳池 #儿童俱乐部 #水疗中心 #私人海滩 #日落景观 #Infinity泳池 #热带雨林景观 #乌布丛林`

**车辆：** `#中文司机 #婴儿座椅 #行李空间大 #全景天窗 #全天候服务 #机场接送 #VIP包车`

**景点：** `#日落观赏点 #浮潜点 #摄影圣地 #稻田风光 #印度教寺庙 #亲子友好 #小众秘境`

**活动：** `#潜水 #冲浪 #火山徒步 #漂流 #丛林探险 #文化体验 #极限运动 #浮潜 #深潜 #ATV #滑索`

**SPA：** `#巴厘岛传统按摩 #四手按摩 #情侣SPA #热石按摩 #排毒疗程 #蜜月套餐 #草本疗法 #花香浴`

**俱乐部：** `#DJ演出 #主题派对 #沙滩酒吧 #VIP包厢 #泳池派对 #现场乐队 #日落美景 #网红打卡`

**餐厅：** `#海鲜烧烤 #海滩景观 #网红餐厅 #蜜月餐厅 #私人包间 #现场音乐 #米其林 #亚洲50佳 #稻田景观`

**下午茶：** `#海景下午茶 #日落下午茶 #泳池下午茶 #花园下午茶 #闺蜜下午茶 #梯田景观 #绝美拍照点`

## 异常处理规范

| 异常类型 | 判断标准 | 处理方式 |
|---------|---------|---------|
| 资源过期 | 合同有效期 < 今天 | 备注"已过期"，可信度降B级 |
| 价格缺失 | 核心价格字段为空 | 暂停入库，告警人工补充 |
| 价格冲突 | 同资源价差 > 10% | 标红，暂停入库，等人工决策 |
| CSV encoding 读取失败 | 所有 encoding 均报错 | 提示用户文件损坏或格式异常 |
| 生产库文件被占用 | PermissionError | 提示用户关闭 Excel / Google Drive Desktop 等程序后再重试 |
| 表头字段不匹配 | 新数据字段与生产库不一致 | 报错退出，不写入，列出缺失/多余字段 |
| GPS缺失 | 坐标字段为空 | 备注"待补充"，不阻止入库 |
| 标签缺失 | 三层标签不完整 | 按资源类型默认补充基础标签 |
| 数据完整度低 | 字段完整度 < 60% | 可信度标C级，优先处理高完整度资源 |

## 参考文档

| 文档 | 路径 |
|------|------|
| 巴厘岛旅游资源标准化文档体系 | `references/巴厘岛旅游资源标准化文档体系.md` |
| 8类特色标签快速查阅表 | `references/8类特色标签快速查阅表.md` |
