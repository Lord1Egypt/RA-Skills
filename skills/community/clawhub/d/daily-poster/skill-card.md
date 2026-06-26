## Description: <br>
Generate two fixed poster variants from minimal JSON with Python: daily for "摸鱼日报" and baidu_hot for "百度热点/百度热搜", with SVG output and optional PNG/JPG/JPEG/WEBP export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[321704933](https://clawhub.ai/user/321704933) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate Chinese daily-news and Baidu hot-search poster assets from compact JSON inputs. It helps an agent choose the correct poster type, prepare valid JSON, and run the renderer for SVG or common raster image outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rendering live posters can make outbound requests to public APIs or remote image hosts. <br>
Mitigation: Run the skill in an isolated Python environment and only render JSON specs and image or API URLs that are trusted. <br>
Risk: Remote API or image URLs could be sensitive in environments where localhost or private-network access is restricted. <br>
Mitigation: Review or restrict URL inputs before execution, especially in network-sensitive environments. <br>
Risk: Renderer execution creates local output and cache files. <br>
Mitigation: Use a controlled output directory and clean generated files when they are no longer needed. <br>
Risk: Unpinned dependency ranges can reduce build reproducibility. <br>
Mitigation: Pin dependency versions when reproducible builds or repeatable image output are required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/321704933/daily-poster) <br>
- [Input schema](references/input-schema.md) <br>
- [Daily poster example spec](references/daily-poster-spec.json) <br>
- [Baidu hot-search example spec](references/baidu-hot-spec.json) <br>
- [2026 holiday countdown data](references/holiday-countdown-2026.json) <br>
- [XXApi provider information](https://xxapi.cn/about) <br>
- [Baidu hot-search API endpoint](https://v2.xxapi.cn/api/baiduhot) <br>
- [2026 China holiday schedule source](https://www.gov.cn/gongbao/2025/issue_12406/202511/content_7048922.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with JSON snippets and shell commands; renderer outputs SVG by default and can also write PNG, JPG, JPEG, or WEBP files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful renderer runs emit stdout JSON describing the requested output, primary output, formats, and rendered file paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
