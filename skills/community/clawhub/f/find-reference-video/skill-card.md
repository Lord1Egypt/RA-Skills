## Description: <br>
从 frameset.app 搜索视频参考片段，找到合集页面和原视频链接。用于： (1) 根据关键词搜索广告/电影片段参考，(2) 获取原视频 YouTube/Vimeo 链接，(3) 下载视频到本地。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FredHNian](https://clawhub.ai/user/FredHNian) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and creative teams use this skill to search Frameset for film or advertising reference clips, review search results, collect source video links, and optionally download selected videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download third-party videos to the user's computer, which may affect storage usage and rights or terms compliance. <br>
Mitigation: Confirm selected videos, filenames, destination, storage impact, and rights or terms considerations before downloading. <br>
Risk: The download workflow depends on yt-dlp and external video links. <br>
Mitigation: Use yt-dlp from a trusted source and review each generated command before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FredHNian/find-reference-video) <br>
- [Frameset search](https://frameset.app/search?search=%E5%85%B3%E9%94%AE%E8%AF%8D) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown table with video links and optional yt-dlp shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose downloads to ~/Downloads/ after user selection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
