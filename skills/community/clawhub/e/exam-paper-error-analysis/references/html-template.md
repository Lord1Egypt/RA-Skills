# HTML Report Structure

**MANDATORY**: 该文件定义了错题分析报告的**内容结构**和**HTML 实现**。

> ⚠️ **依赖说明**：本文件第4节（错题逐题分析）引用 `error-types.md` 中的六类错误定义。
> 如果你尚未在当前会话中加载 `error-types.md`，请在读取本文件前或之后立即加载。

## 内容结构定义（所有子能力共用）

HTML 报告**必须包含以下全部 6 个部分**，所有章节的 HTML 结构（标题、id 锚点、容器 div）都必须出现在最终输出中。
内容根据触发子能力填充：
- **触发的子能力**：填充完整分析内容
- **未触发的子能力**：对应章节填充"本次分析未涉及此模块"，但仍保留章节标题和锚点结构

### 1. 试卷/试题基本信息
- 年级、学科、分析日期
- 分析类型（单题深度分析 / 整卷失分分析 / 变式题生成 / 错题分类讲评）
- 试卷名称、满分分值

### 2. 导航目录
- 粘性定位（sticky TOC）
- 分组结构：整卷失分分析、错题逐题分析、变式练习、错题分类讲评
- 锚点链接跳转到各章节

### 3. 整卷失分分析（触发子能力2时显示）
- **失分地图**：知识点/能力维度表格（失分、涉及题号、失分率、对应岗位能力）
- **提分优先级**：3 个优先补强项（原因 + 最小可执行训练方案）

### 4. 错题逐题分析（触发子能力1时显示）
每道题包含七步框架 `error-types.md`：
1. 这道题考查的核心能力
2. 学生错误答案暴露出的可能问题（6 个维度）
3. 最可能的错误原因排序
4. 可以追问学生的 3 个问题
5. 后续可以设计的 3 道变式练习
- **职业教育增强**：当学科为职教课程时，追加第八步"职业能力发展建议"（**MANDATORY - READ** `vocational-standards.md` 获取岗位能力模型）

### 5. 变式练习（触发子能力3时显示）
- 基础巩固题（题目 + 设计意图 + 标准步骤 + 常见坑）
- 易错辨析题（结构同上）
- 迁移应用题（结构同上）

### 6. 错题分类讲评（触发子能力4时显示）
- 错题分类统计（6 类错误类型表格）
| 错误类型 | 题号 | 人数/比例 | 典型表现 |
|---------|------|----------|---------|
| 知识不会型 | [N] | [X]人/[X]% | [描述] |
| 概念混淆型 | [N] | [X]人/[X]% | [描述] |
| 审题粗心型 | [N] | [X]人/[X]% | [描述] |
| 方法断裂型 | [N] | [X]人/[X]% | [描述] |
| 表达不完整型 | [N] | [X]人/[X]% | [描述] |
| 迁移失败型 | [N] | [X]人/[X]% | [描述] |



- 分类讲评策略（老师讲评时应该重点讲什么：每类错误对应讲评方法）

 知识不会型 → 补关键知识
[具体讲评方法：补哪个知识点，怎么补]

概念混淆型 → 对比辨析
[具体讲评方法：对比哪两个易混淆概念，怎么辨析]

 审题粗心型 → 训练读题方法
[具体讲评方法：训练圈画关键词、转述题意等读题技能]

方法断裂型 → 补过程支架
[具体讲评方法：补充哪一步的思维支架，怎么搭建]

表达不完整型 → 给答题句式
[具体讲评方法：提供答题模板或句式框架]

迁移失败型 → 做变式练习
[具体讲评方法：设计什么类型的变式题，怎么检验迁移能力]

- 讲评优先级建议
[基于失分率和重要性的讲评顺序建议。优先讲评失分率高、影响后续学习的题目。]


---

## HTML 格式实现

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>错题分析报告 - [年级][学科]</title>
    <style>
        /* 内联样式：排版、颜色、TOC、卡片、打印样式 */
    </style>
</head>
<body>
    <div class="container">
        <!-- 1. 试卷/试题基本信息 -->
        <h1>错题分析报告</h1>
        <div class="meta">
            <p><strong>年级</strong>：[年级] | <strong>学科</strong>：[学科] | <strong>分析日期</strong>：[日期]</p>
            <p><strong>分析类型</strong>：[单题深度分析 / 整卷失分分析 / 变式题生成 / 错题分类讲评]</p>
            <p><strong>试卷名称</strong>：[试卷名称] | <strong>满分</strong>：[满分]分</p>
        </div>
        
        <!-- 2. 导航目录 -->
        <div class="toc">
            <h3> 目录</h3>
            <div class="section-group">
                <div class="section-title">📊 整卷失分分析</div>
                <ul class="sub-items">
                    <li><a href="#paper-loss-map">一、失分地图</a></li>
                    <li><a href="#paper-priority">二、提分优先级</a></li>
                </ul>
            </div>
            <div class="section-group">
                <div class="section-title"> 错题逐题分析</div>
                <ul class="sub-items">
                    <li><a href="#q1">第 1 题深度分析</a></li>
                    <li><a href="#q2">第 2 题深度分析</a></li>
                    <!-- 更多题目... -->
                </ul>
            </div>
            <div class="section-group">
                <div class="section-title">📝 变式练习</div>
                <ul class="sub-items">
                    <li><a href="#variant-basic">一、基础巩固题</a></li>
                    <li><a href="#variant-discriminate">二、易错辨析题</a></li>
                    <li><a href="#variant-transfer">三、迁移应用题</a></li>
                </ul>
            </div>
            <div class="section-group">
                <div class="section-title">📋 错题分类讲评</div>
                <ul class="sub-items">
                    <li><a href="#class-stats">一、错题分类统计</a></li>
                    <li><a href="#class-strategy">二、分类讲评策略</a></li>
                    <li><a href="#class-priority">三、讲评优先级建议</a></li>
                </ul>
            </div>
        </div>
        
        <!-- 3. 整卷失分分析（SKILL.md 256-280行） -->
        <h2 id="paper-loss-map">一、失分地图[（按能力维度）]</h2>
        <table>
            <tr><th>知识点/能力维度</th><th>失分</th><th>涉及题号</th><th>失分率</th><th>[对应岗位能力]</th></tr>
            <tr><td>[维度 1]</td><td>[X]分</td><td>第 [N] 题</td><td>[X]%</td><td>[职教：岗位能力]</td></tr>
        </table>
        
        <h2 id="paper-priority">二、提分优先级</h2>
        <ol>
            <li><strong>优先补 [能力/知识点]</strong> — [原因] — [最小可执行训练方案，每天≤15 分钟，职教：以实操为主]</li>
            <li>...</li>
            <li>...</li>
        </ol>
        
        <hr class="section-divider">
        
        <!-- 4. 错题逐题分析（SKILL.md 192-229行） -->
        <h2 id="q1">第 1 题深度分析</h2>
        
        <h3>一、这道题考查的核心能力</h3>
        <p>[说明真正考的是什么，结合学科特点分析深层能力要求]</p>
        
        <h3>二、学生错误答案暴露出的可能问题</h3>
        <p><strong>1. 知识点是否掌握</strong> [分析]</p>
        <p><strong>2. 概念是否存在误解</strong> [分析]</p>
        <p><strong>3. 审题是否出现偏差</strong> [分析]</p>
        <p><strong>4. 解题步骤或思维过程哪里断了</strong> [分析]</p>
        <p><strong>5. 表达是否不完整</strong> [分析]</p>
        <p><strong>6. 是否存在迁移困难</strong> [分析]</p>
        
        <h3>三、最可能的错误原因排序</h3>
        <ol><li>[原因] — 可能性[高/中/低] — [理由，需有证据支撑]</li></ol>
        
        <h3>四、老师讲评时应该重点讲什么</h3>
        <p>[具体到知识点、方法、思维步骤]</p>
        
        <h3>五、可以追问学生的 3 个问题</h3>
        <ol><li>[问题 1]</li><li>[问题 2]</li><li>[问题 3]</li></ol>
        
        <h3>六、后续可以设计的 3 道变式练习</h3>
        <div class="question-card"><h4>1. 基础巩固题</h4><p>[题目]</p><p><strong>设计意图</strong>：[针对什么薄弱点]</p></div>
        <div class="question-card"><h4>2. 易错辨析题</h4><p>[题目]</p><p><strong>设计意图</strong>：[辨析什么易混淆点]</p></div>
        <div class="question-card"><h4>3. 迁移应用题</h4><p>[题目]</p><p><strong>设计意图</strong>：[在什么新情境中应用]</p></div>
        
        <div class="tip"><h3>七、给老师的一句话提醒</h3><p>[一句话，精准有力]</p></div>
        
        <hr class="section-divider">
        
        <!-- 第 2 题、第 N 题（同上结构） -->
        <h2 id="q2">第 2 题深度分析</h2>
        <p>[同上结构]</p>
        
        <hr class="section-divider">
        
        <!-- 5. 变式练习（SKILL.md 304-319行） -->
        <h2 id="variant-basic">一、基础巩固题（[N]道）</h2>
        <div class="question-card">
            <h4>题 1</h4>
            <p>[题目]</p>
            <p><strong>设计意图</strong>：[针对什么薄弱点]</p>
            <p><strong>标准步骤</strong>：[解题过程]</p>
            <p><strong>常见坑</strong>：[学生容易犯的错误]</p>
        </div>
        
        <h2 id="variant-discriminate">二、易错辨析题（[N]道）</h2>
        <div class="question-card">
            <h4>题 1</h4>
            <p>[题目]</p>
            <p><strong>设计意图</strong>：[辨析什么易混淆点]</p>
            <p><strong>标准步骤</strong>：[解题过程]</p>
            <p><strong>常见坑</strong>：[学生容易犯的错误]</p>
        </div>
        
        <h2 id="variant-transfer">三、迁移应用题（[N]道）</h2>
        <div class="question-card">
            <h4>题 1</h4>
            <p>[题目]</p>
            <p><strong>设计意图</strong>：[在什么新情境中应用]</p>
            <p><strong>标准步骤</strong>：[解题过程]</p>
            <p><strong>常见坑</strong>：[学生容易犯的错误]</p>
        </div>
        
        <hr class="section-divider">
        
        <!-- 6. 错题分类讲评建议（error-types.md 231-253行） -->
        <h2 id="class-stats">一、错题分类统计</h2>
        <table>
            <tr><th>错误类型</th><th>题号</th><th>人数/比例</th><th>典型表现</th></tr>
            <tr><td>知识不会型</td><td>[N]</td><td>[X]人/[X]%</td><td>[描述]</td></tr>
            <tr><td>概念混淆型</td><td>[N]</td><td>[X]人/[X]%</td><td>[描述]</td></tr>
            <tr><td>审题粗心型</td><td>[N]</td><td>[X]人/[X]%</td><td>[描述]</td></tr>
            <tr><td>方法断裂型</td><td>[N]</td><td>[X]人/[X]%</td><td>[描述]</td></tr>
            <tr><td>表达不完整型</td><td>[N]</td><td>[X]人/[X]%</td><td>[描述]</td></tr>
            <tr><td>迁移失败型</td><td>[N]</td><td>[X]人/[X]%</td><td>[描述]</td></tr>
        </table>
        
        <h2 id="class-strategy">二、分类讲评策略</h2>
        <ul>
            <li>知识不会型 → 补关键知识（见 error-types.md 第1节）</li>
            <li>概念混淆型 → 对比辨析（见 error-types.md 第2节）</li>
            <li>审题粗心型 → 训练读题方法（见 error-types.md 第3节）</li>
            <li>方法断裂型 → 补过程支架（见 error-types.md 第4节）</li>
            <li>表达不完整型 → 给答题句式（见 error-types.md 第5节）</li>
            <li>迁移失败型 → 做变式练习（见 error-types.md 第6节）</li>
        </ul>
        
        <h2 id="class-priority">三、讲评优先级建议</h2>
        <p>[基于失分率和重要性的讲评顺序]</p>
        
        <div class="footer"><p>由 <strong>exam-paper-error-analysis</strong> 技能生成 | [日期]</p></div>
    </div>
</body>
</html>
```
