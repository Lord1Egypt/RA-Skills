## Description: <br>
Shopify 网店分类链接采集器 - 自动从导航提取真实分类层级，处理 Ajax 懒加载下拉菜单，一级分类二级分类分别放在不同单元格，输出 CSV。支持 Shopify 多级别分类导航。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QirongZhang](https://clawhub.ai/user/QirongZhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ecommerce operators use this skill to collect Shopify-style storefront category links, preserve navigation hierarchy, and export the results for spreadsheet review or downstream catalog analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill crawls storefront pages and may be inappropriate for sites where the user lacks authorization. <br>
Mitigation: Run it only against sites you are authorized to crawl and respect the site's applicable policies. <br>
Risk: npm dependency resolution can introduce ordinary supply-chain risk. <br>
Mitigation: Install from the reviewed package and lockfile using a trusted npm registry. <br>
Risk: The saved homepage screenshot may capture visible page state, including sensitive information if the browser is authenticated. <br>
Mitigation: Run from a non-sensitive browsing context and avoid authenticated storefront or admin views when collecting screenshots. <br>
Risk: CSV and screenshot files are written to a local output directory. <br>
Mitigation: Choose the output directory deliberately and handle generated files according to the site's data sensitivity. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QirongZhang/category-collector) <br>
- [Artifact README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with command examples; CSV and PNG files created by the collection script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CSV output includes category URLs, slugs, hierarchy columns, and depth; the tool may also save a homepage screenshot.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
