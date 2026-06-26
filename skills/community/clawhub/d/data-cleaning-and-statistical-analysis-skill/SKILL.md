# Data Cleaning and Statistical Analysis Skill

## Purpose

This skill supports data cleaning, quality checking, statistical analysis, and academic interpretation of quantitative datasets. It is especially useful for experimental psychology, clinical research, behavioral science, education research, questionnaire studies, and project-based data analysis.

## When to Use

Use this skill when the user needs help with:

- Cleaning raw CSV, Excel, SPSS-exported, PsychoPy, PsychoJS, or online experiment data.
- Checking whether behavioral data are valid or usable.
- Identifying missing values, duplicate rows, abnormal reaction times, impossible responses, or coding problems.
- Splitting or merging datasets.
- Creating derived variables such as accuracy, mean reaction time, omission errors, commission errors, learning scores, block-level performance, or change scores.
- Selecting statistical tests based on research design.
- Running descriptive statistics, t-tests, ANOVA, repeated-measures ANOVA, mixed ANOVA, correlation, regression, chi-square tests, or nonparametric tests.
- Explaining statistical results in academic language.

## Inputs

The user may provide:

- A dataset file such as `.csv`, `.xlsx`, `.sav`, or `.tsv`.
- A description of the study design.
- Variable names and coding rules.
- Grouping information, such as patient group vs healthy control group.
- Experimental condition labels, such as block, trial type, congruent/incongruent, target/non-target, or pre/post.
- Required output format, such as APA style, thesis writing, tables, graphs, or plain-language explanation.

## Core Workflow

### 1. Understand the Research Design

Before analysis, identify:

- Whether the design is between-subjects, within-subjects, mixed, cross-sectional, longitudinal, or pre-post.
- What the independent variables are.
- What the dependent variables are.
- Whether the main research question is group difference, condition difference, association, prediction, or change over time.
- Whether the data come from behavioral tasks, questionnaires, clinical scales, or physiological measures.

### 2. Inspect the Dataset

Check:

- Number of rows and columns.
- Variable names.
- Data types.
- Missing values.
- Duplicate participant IDs.
- Unexpected category labels.
- Range and distribution of key variables.
- Whether trial numbers and block numbers match the intended experimental design.

### 3. Clean the Data

Common cleaning steps include:

- Removing practice trials when formal analysis should only include experimental trials.
- Excluding invalid trials, such as no response, timeout, or incorrect response when reaction time analysis requires correct trials only.
- Filtering implausible reaction times according to task-specific rules.
- Recoding categorical variables.
- Creating participant-level summary scores.
- Calculating condition-level means and accuracy.
- Checking whether each participant has enough valid trials.

### 4. Choose Statistical Tests

Select tests according to the design:

- Two independent groups: independent-samples t-test or Mann-Whitney U test.
- Two paired conditions: paired-samples t-test or Wilcoxon signed-rank test.
- More than two repeated conditions: repeated-measures ANOVA or Friedman test.
- Group × Condition design: mixed ANOVA or linear mixed model.
- Association between variables: Pearson or Spearman correlation.
- Prediction model: linear regression, logistic regression, or mixed-effects regression.
- Categorical variables: chi-square test or Fisher's exact test.

### 5. Report Results

Results should include:

- Descriptive statistics.
- Test statistic.
- Degrees of freedom when applicable.
- p value.
- Effect size.
- Confidence interval when appropriate.
- Interpretation linked to the research hypothesis.

## Output Requirements

The assistant should provide:

- A clear summary of data quality.
- Cleaning decisions and exclusion criteria.
- A table of key descriptive statistics when useful.
- Recommended statistical tests with justification.
- Interpretable results in academic language.
- Warnings when the data structure does not match the intended design.
- Suggestions for improving data collection or coding if problems are found.

## Style Guidelines

- Be transparent about assumptions.
- Do not overclaim statistical significance.
- Distinguish between descriptive trends and statistically significant findings.
- Explain statistical concepts in accessible language when the user is a beginner.
- Use academic wording when the user is preparing a thesis, report, or ethics application.
- Preserve original data unless the user explicitly asks for a cleaned file.

## Example User Requests

- "帮我检查这个 CPT 数据是否正确。"
- "请帮我清洗 PsychoPy 导出的数据，并计算每个 block 的正确率和反应时。"
- "我的研究是患者组和健康组在四个 block 中的表现差异，应该用什么统计方法？"
- "帮我把这个数据整理成 SPSS 可以分析的格式。"
- "根据这个结果帮我写 APA 风格的统计结果。"
