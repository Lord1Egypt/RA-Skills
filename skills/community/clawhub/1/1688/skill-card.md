## Description: <br>
从淘宝/1688下载商品图片。触发词：淘宝下载图片、1688下载图片、商品图片下载、淘宝主图、下载商品图、1688图片。支持通过商品名搜索或直接提供商品URL下载主图和详情图。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gufusheng1994-dev](https://clawhub.ai/user/gufusheng1994-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketplace sellers, sourcing teams, and agents use this skill to collect main, color, and detail images from Taobao or 1688 product pages by URL or product-name search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browsing Taobao or 1688 can involve shopping-site cookies or logged-in sessions. <br>
Mitigation: Use a clean browser profile when you do not want shopping-site cookies or account sessions involved. <br>
Risk: Downloaded product images may be saved into local or shared folders. <br>
Mitigation: Choose a non-shared output directory when product images or sourcing information should remain private. <br>
Risk: Anti-hotlinking, lazy loading, or login requirements can make downloaded image sets incomplete. <br>
Mitigation: Review the download summary, saved paths, and failed image list before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gufusheng1994-dev/1688) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, files] <br>
**Output Format:** [Markdown-style agent instructions with shell and browser command examples, plus downloaded image files and a text download summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads are organized by product and image category, with reported counts, file sizes, save paths, and failures when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
