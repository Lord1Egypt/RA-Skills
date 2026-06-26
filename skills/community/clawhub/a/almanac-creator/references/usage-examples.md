# 黄历制作技能 - 使用示例

## 🎯 快速开始

### 基本用法

```bash
# 生成今日黄历（默认 3 页）
python skills/almanac-creator/scripts/generate_almanac.py --date 2026-04-08

# 生成指定日期黄历
python skills/almanac-creator/scripts/generate_almanac.py --date 2026-04-09 --pages 3

# 仅生成第 1 页（抖音用）
python skills/almanac-creator/scripts/generate_almanac.py --date 2026-04-08 --pages 1

# 指定输出目录
python skills/almanac-creator/scripts/generate_almanac.py --date 2026-04-08 --output ./output
```

### 参数说明

| 参数 | 说明 | 默认值 | 选项 |
|------|------|--------|------|
| `--date` | 日期（YYYY-MM-DD） | 今天 | 任意有效日期 |
| `--pages` | 生成页数 | 3 | 1/2/3 |
| `--output` | 输出目录 | reports/ | 任意目录路径 |

---

## 📝 完整工作流示例

### 示例 1：日常黄历制作

```bash
# 1. 生成黄历图片（3 页）
python skills/almanac-creator/scripts/generate_almanac.py --date 2026-04-08

# 输出：
# [OK] 第 1 页已保存：reports/2026-04-08_黄历.png
# [OK] 第 2 页已保存：reports/2026-04-08_黄历_养生.png
# [OK] 第 3 页已保存：reports/2026-04-08_黄历_故事.png
```

### 示例 2：批量生成未来 7 天黄历

```bash
# 创建批量生成脚本
python -c "
import os
from datetime import datetime, timedelta

for i in range(7):
    date = datetime.now() + timedelta(days=i)
    date_str = date.strftime('%Y-%m-%d')
    os.system(f'python skills/almanac-creator/scripts/generate_almanac.py --date {date_str}')
"
```

### 示例 3：接入黄历 API 获取真实数据

修改 `generate_almanac.py` 中的 `get_almanac_data()` 函数：

```python
import requests

def get_almanac_data(date_str):
    """从 API 获取黄历数据"""
    try:
        # 使用青云客 API
        response = requests.get(
            'https://api.qingyunke.com/api.php',
            params={'key': 'free', 'appid': '01', 'msg': '今日黄历'}
        )
        data = response.json()
        
        # 解析 API 返回数据
        return {
            'date_gregorian': f"{date_str} 星期三",
            'date_lunar': data['content']['lunar'],  # 根据实际 API 调整
            'special_day': "清明节气第 3 天",
            'yi': data['content']['yi'],
            'ji': data['content']['ji'],
            # ... 其他字段
        }
    except Exception as e:
        print(f"API 获取失败：{e}")
        # 返回默认数据
        return get_default_data()
```

---

## 🎨 自定义样式

### 修改颜色方案

编辑 `generate_almanac.py` 中的 `COLORS` 字典：

```python
COLORS = {
    'china_red': '#8B0000',      # 中国红
    'bright_red': '#C41E3A',     # 亮红色
    'ink_black': '#2C2C2C',      # 墨黑色
    'gold': '#D4AF37',           # 金色
    'light_gray': '#999999',     # 浅灰色
    'pale_gray': '#CCCCCC'       # 极浅灰
}
```

### 修改字体大小

编辑 `FONT_SIZES` 字典：

```python
FONT_SIZES = {
    'title': 90,      # 主标题
    'subtitle': 65,   # 副标题
    'section': 55,    # 栏目题
    'content': 45,    # 正文
    'small': 38       # 小字
}
```

---

## 📱 发布流程

### 今日头条发布

1. **准备材料**:
   - 3 张黄历图片
   - 发布文案（见下方模板）

2. **发布步骤**:
   - 打开今日头条 APP
   - 点击"发布" → "图文"
   - 上传 3 张图片（按顺序）
   - 粘贴文案
   - 添加话题标签
   - 点击发布

3. **文案模板**:
```
【2026 年 04 月 08 日】农历丙午年 二月三十 每日黄历

今日黄历已更新！

📅 公历：2026 年 04 月 08 日 星期三
🌙 农历：农历丙午年 二月三十
🌱 节气：清明节气第 3 天

✅ 宜：祭祀 祈福 开市 交易 纳财 入宅 安床 栽种
❌ 忌：动土 破土 安葬 行丧 词讼 开仓

🏆 红榜生肖：
🥇 生肖兔：六合吉日，贵人相助，诸事顺利
🥈 生肖羊：三合助力，财运亨通，合作愉快  
🥉 生肖虎：寅亥相合，事业有成，家庭和睦

⚠️ 黑榜生肖：
🐍 生肖蛇：巳亥相冲，诸事不顺，谨言慎行
🐷 生肖猪：亥亥自刑，情绪波动，注意健康
🐒 生肖猴：申亥相害，小人暗算，防备损失

财神方位：东南方 | 喜神方位：西南方 | 福神方位：正东方

更多详细内容见图👆

#每日黄历 #传统文化 #生肖运势 #清明节气
```

### 抖音发布

1. **准备材料**:
   - 第 1 页黄历图片
   - 背景音乐（推荐国风类）
   - 发布文案

2. **发布步骤**:
   - 打开抖音 APP
   - 点击"+" → "上传"
   - 选择黄历图片
   - 添加背景音乐
   - 粘贴文案
   - 添加话题标签
   - 点击发布

3. **文案模板**:
```
【4 月 8 日黄历】清明时节，宜祭祀祈福✨

今日红榜生肖：兔、羊、虎
黑榜生肖：蛇、猪、猴

财神在东南方，记得朝这个方向求财哦💰

传统文化仅供参考，转发给需要的朋友吧！

#黄历 #每日运势 #传统文化 #清明节 #生肖运势
```

---

## ⚠️ 常见问题

### Q1: 文件名为乱码怎么办？

**A**: Windows 系统编码问题，不影响使用。可通过 Python 脚本查看真实文件名：

```python
import os
files = [f for f in os.listdir('reports') if '2026-04-08' in f]
for f in files:
    print(f)
```

### Q2: 文件大小超过 250KB 怎么办？

**A**: 调整图片压缩参数：

```python
# 在 generate_almanac.py 中修改
img.save(filepath, 'PNG', quality=90, optimize=True)
```

### Q3: 如何更换字体？

**A**: 修改 `load_fonts()` 函数中的字体路径：

```python
# Mac 系统
fonts = {
    'title': ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', 90),
    # ... 其他字体
}

# Linux 系统
fonts = {
    'title': ImageFont.truetype('/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc', 90),
    # ... 其他字体
}
```

### Q4: 如何自动化每日发布？

**A**: 使用 Windows 任务计划程序：

1. 创建批处理文件 `daily_almanac.bat`:
```batch
@echo off
cd C:\Users\liuyan\.openclaw\workspace
python skills/almanac-creator/scripts/generate_almanac.py --date %date:~0,4%-%date:~5,2%-%date:~8,2%
```

2. 打开任务计划程序
3. 创建基本任务
4. 设置每日 05:00 执行
5. 选择 `daily_almanac.bat`

---

## 📊 质量检查清单

发布前请检查：

- [ ] 图片尺寸 1080x1400
- [ ] 双层边框完整（外红内金）
- [ ] 文字居中对齐
- [ ] 无错别字
- [ ] 文件大小 150-250KB
- [ ] 底部免责声明存在
- [ ] 日期信息准确
- [ ] 宜忌内容完整
- [ ] 生肖运势正确（红黑榜各 3 个）

---

## 🔗 相关资源

- **技能文档**: `skills/almanac-creator/SKILL.md`
- **制作标准**: `skills/almanac-creator/references/almanac-image-standard.md`
- **生成脚本**: `skills/almanac-creator/scripts/generate_almanac.py`
- **复盘文档**: `memory/黄历制作复盘/2026-04-08 黄历制作流程复盘.md`

---

*文档创建时间：2026-04-08 11:23*  
*适用范围：黄历制作技能使用指导*  
*版本：V1*
