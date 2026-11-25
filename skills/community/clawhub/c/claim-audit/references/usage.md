# 三种用法

## 一、发版前自查

发布任何技能包之前跑一遍，确认 README 里的数字没漂：

```bash
python scripts/audit.py check D:\doubao\_matrix_v3\evidence-anchor
```

输出 7 条声明全部 OK，退出码 0，才允许提交。

## 二、接手别人的包

只想知道对方声明了什么，不跑任何东西：

```bash
python scripts/audit.py list D:\doubao\_matrix_v3\skill-improver
```

输出会列出每条声明的来源文件与原文，末尾写明"仅列出，未核验"。

## 三、接进流水线

要机器可读结果：

```bash
python scripts/audit.py check D:\path\to\pkg --json --strict
```

`--json` 输出 `total / mismatch / unverifiable / rows` 四个字段；`--strict` 让 `UNVERIFIABLE` 也返回 1。两者组合适合放进 CI，把"文档数字漂移"当构建失败处理。

## 真实输出

```text
声明 7 条：对上 7，对不上 0，验不了 0
```

对不上时：

```text
tests      MISMATCH 7/9          自检全部通过（9/9 PASS）
```
