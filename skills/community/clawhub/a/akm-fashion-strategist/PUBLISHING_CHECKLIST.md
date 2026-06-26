<!--
文件：PUBLISHING_CHECKLIST.md
核心功能：作为 Fashion 分支公开发布前的英文检查清单，避免私有资产泄露、口径错位和结构缺失。
输入：Fashion 分支当前 skill 包、论文稿与发布页文案。
输出：供发布前逐项核对的英文检查清单。
-->

# Fashion Publishing Checklist

## Framing

- [ ] title clearly identifies this as the Fashion branch of AKM rather than a standalone parent concept
- [ ] claims do not drift into image-recognition, virtual try-on, or broad benchmark language
- [ ] paper framing is consistent with a method paper under scene and asset constraints

## Privacy

- [ ] no full private wardrobe inventory is exposed
- [ ] no identity-specific body or styling details are exposed
- [ ] style preferences are rewritten as reusable input fields rather than named self-description

## Structure

- [ ] `ELICITATION_PROMPT.md` is readable on its own
- [ ] `RECORD_TEMPLATE.md` is reusable on its own
- [ ] `EXECUTION_PROMPT.md` does not conflict with the other two
- [ ] `SKILL.md` makes it explicit that the method is not a single prompt
- [ ] store copy and skill copy use the same framing
