# 苏服采交互式采集流程

## 概览
本文档描述苏服采网站的交互式采集流程，通过脚本执行操作、智能体分析截图的闭环方式完成复杂的数据采集任务。

## 适用场景
- 苏服采网站需要复杂的交互操作（登录、三级地区选择、搜索勾选等）
- 自动化脚本难以处理动态页面和复杂交互
- 需要灵活适应页面变化和异常情况

## 流程概述
采用"操作 → 截图 → 分析 → 决策 → 操作"的循环模式：
1. 脚本执行操作（打开页面、点击、输入等）
2. 脚本截图返回当前页面状态
3. 智能体分析截图，理解当前状态
4. 智能体根据分析结果决定下一步操作
5. 循环执行，直到完成采集

## 详细操作步骤

### 步骤 1: 初始化浏览器
**操作**:
```bash
python scripts/sufu_interactive.py --action open --url "https://js.fwgov.cn/bidding?serviceType=1" --headless false
```

**预期结果**: 浏览器打开苏服采网站

**决策点**:
- 如果页面正常加载 → 进入步骤 2
- 如果显示登录界面 → 需要处理登录（暂不支持，跳过苏服采）
- 如果页面加载失败 → 等待后重试

### 步骤 2: 等待页面稳定并截图
**操作**:
```bash
python scripts/sufu_interactive.py --action wait --wait-time 2000
python scripts/sufu_interactive.py --action screenshot --screenshot-name "step1_initial.png"
```

**预期结果**: 获取初始页面截图

**分析重点**:
- 检查是否有地区选择框（通常在页面顶部）
- 识别选择框的数量和位置
- 检查是否需要登录

### 步骤 3: 识别地区选择框
**分析截图**:
- 查找地区选择相关元素（省、市、区三级选择框）
- 确认选择框是否可见
- 识别选择框的当前状态

**操作（如果需要点击地区选择）**:
```bash
python scripts/sufu_interactive.py --action click --selector ".ivu-select-visible" --timeout 5000
python scripts/sufu_interactive.py --action screenshot --screenshot-name "step2_select_opened.png"
```

### 步骤 4: 选择江苏省
**操作（如果需要在第一个选择框选择江苏省）**:
```bash
python scripts/sufu_interactive.py --action click --selector ".ivu-select-dropdown .ivu-select-item" --timeout 5000
python scripts/sufu_interactive.py --action screenshot --screenshot-name "step3_province_selected.png"
```

**决策点**:
- 如果江苏省已选中或不需要选择 → 进入步骤 5
- 如果需要重新选择 → 点击正确的选项后截图

### 步骤 5: 选择盐城市
**操作（如果需要在第二个选择框选择盐城市）**:
```bash
# 点击第二个选择框
python scripts/sufu_interactive.py --action click --selector ".ivu-select:nth-of-type(2)" --timeout 5000
python scripts/sufu_interactive.py --action wait --wait-time 1000

# 点击盐城市
python scripts/sufu_interactive.py --action click --selector ".ivu-select-dropdown .ivu-select-item" --timeout 5000
python scripts/sufu_interactive.py --action screenshot --screenshot-name "step4_city_selected.png"
```

### 步骤 6: 选择盐南高新区和经开区（复选框）
**操作**:
```bash
# 点击第三个选择框（复选框）
python scripts/sufu_interactive.py --action click --selector ".ivu-select:nth-of-type(3)" --timeout 5000
python scripts/sufu_interactive.py --action wait --wait-time 1000
python scripts/sufu_interactive.py --action screenshot --screenshot-name "step5_dropdown_opened.png"

# 第二次点击，激活输入框
python scripts/sufu_interactive.py --action click --selector ".ivu-select:nth-of-type(3)" --timeout 5000
python scripts/sufu_interactive.py --action wait --wait-time 500
python scripts/sufu_interactive.py --action screenshot --screenshot_name "step6_input_activated.png"
```

**分析截图**:
- 检查是否出现输入框
- 识别输入框的位置和状态
- 检查是否有搜索建议或下拉列表

**操作（输入"盐南高新区"）**:
```bash
python scripts/sufu_interactive.py --action input --selector ".ivu-select-dropdown input" --text "盐南高新区" --timeout 5000
python scripts/sufu_interactive.py --action wait --wait-time 1000
python scripts/sufu_interactive.py --action screenshot --screenshot-name "step7_search_yannan.png"
```

**分析截图**:
- 检查搜索结果是否出现
- 识别"盐南高新区"选项
- 确认选项的完整文本（可能是"江苏省 / 盐城市 / 盐南高新区"）

**操作（勾选盐南高新区）**:
```bash
# 点击搜索结果中的盐南高新区选项
python scripts/sufu_interactive.py --action click --selector ".ivu-select-item" --timeout 5000
python scripts/sufu_interactive.py --action wait --wait-time 500
python scripts/sufu_interactive.py --action screenshot --screenshot-name "step8_yannan_selected.png"
```

**操作（输入"经开区"）**:
```bash
python scripts/sufu_interactive.py --action input --selector ".ivu-select-dropdown input" --text "经开区" --timeout 5000
python scripts/sufu_interactive.py --action wait --wait-time 1000
python scripts/sufu_interactive.py --action screenshot --screenshot-name "step9_search_jingkai.png"
```

**操作（勾选经开区）**:
```bash
# 点击搜索结果中的经开区选项
python scripts/sufu_interactive.py --action click --selector ".ivu-select-item" --timeout 5000
python scripts/sufu_interactive.py --action wait --wait-time 500
python scripts/sufu_interactive.py --action screenshot --screenshot-name "step10_jingkai_selected.png"
```

### 步骤 7: 隐藏下拉框并等待页面刷新
**操作**:
```bash
# 点击页面空白处
python scripts/sufu_interactive.py --action click-coords --x 500 --y 500
python scripts/sufu_interactive.py --action wait --wait-time 2000
python scripts/sufu_interactive.py --action screenshot --screenshot-name "step11_after_select.png"
```

**分析截图**:
- 检查下拉框是否关闭
- 检查页面是否显示筛选结果
- 验证地区选择是否生效（URL或页面元素是否包含选定区域）

### 步骤 8: 提取招投标数据
**操作**:
```bash
# 使用JavaScript提取页面数据
python scripts/sufu_interactive.py --action script --script "
(function() {
    const items = document.querySelectorAll('.ivu-card, .ivu-list-item, [class*=\"project\"], [class*=\"bidding\"]');
    const results = [];
    items.forEach(item => {
        const title = item.querySelector('[class*=\"title\"], [class*=\"name\"], h3, h4, a');
        const date = item.querySelector('[class*=\"date\"], [class*=\"time\"]');
        const link = item.querySelector('a');
        if (title || link) {
            results.push({
                title: title ? title.innerText.trim() : '',
                date: date ? date.innerText.trim() : '',
                link: link ? link.href : ''
            });
        }
    });
    return results;
})()
"
```

**预期结果**: 返回提取的项目列表（JSON格式）

**分析提取结果**:
- 检查数据数量
- 验证项目标题是否包含盐南高新区或经开区
- 检查日期是否在采集范围内
- 确认链接是否有效

### 步骤 9: 验证数据准确性
**分析重点**:
- 所有项目都应属于盐南高新区或经开区
- 项目状态应为"招标中"或"进行中"，不包括"响应截止"
- 项目标题应清晰，无乱码
- 日期应准确

**如果数据不准确**:
- 返回步骤 6，重新执行地区选择
- 检查是否有遗漏的选项
- 调整搜索关键词

### 步骤 10: 保存数据并关闭浏览器
**操作**:
```bash
# 获取最终截图
python scripts/sufu_interactive.py --action screenshot --screenshot-name "step12_final.png"

# 关闭浏览器
python scripts/sufu_interactive.py --action close
```

## 脚本操作命令参考

### 基础操作
- `--action open`: 打开页面
- `--action screenshot`: 截图
- `--action click`: 点击元素
- `--action click-coords`: 通过坐标点击
- `--action input`: 输入文本
- `--action wait`: 等待
- `--action wait-element`: 等待元素出现
- `--action script`: 执行JavaScript
- `--action close`: 关闭浏览器

### 常用参数
- `--url`: 要打开的URL
- `--selector`: CSS选择器
- `--text`: 要输入的文本
- `--x`, `--y`: 点击坐标
- `--timeout`: 等待超时时间（毫秒）
- `--wait-time`: 等待时间（毫秒）
- `--script`: JavaScript代码
- `--screenshot-name`: 截图文件名
- `--headless`: 是否无头模式（true/false）

## 注意事项
1. **截图优先**: 每次重要操作后都要截图，便于智能体分析当前状态
2. **等待时间**: 页面加载和异步操作需要适当的等待时间
3. **选择器灵活性**: 根据实际页面结构调整CSS选择器
4. **异常处理**: 如果操作失败，分析截图后调整策略
5. **数据验证**: 提取数据后必须验证其准确性和完整性

## 调试技巧
- 使用 `--headless false` 模式可以看到实际浏览器操作
- 每步操作后截图，便于回溯和分析
- 使用浏览器开发者工具获取准确的CSS选择器
- 记录每个步骤的输入和输出，便于问题定位
