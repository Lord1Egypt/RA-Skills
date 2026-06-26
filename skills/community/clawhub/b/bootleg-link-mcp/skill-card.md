## Description: <br>
Bootleg Link MCP is an MCP server for downloading and managing YouTube, Qobuz, and Beatport music workflows with CDJ-2000 compatible MP3 output, resumable queues, browser-based logins, and a bgutil PO token helper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[esanle](https://clawhub.ai/user/esanle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate an MCP-controlled music downloader for YouTube preview downloads, Qobuz and Beatport account workflows, task tracking, and CDJ-ready audio file output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles local account and session material for music services. <br>
Mitigation: Use dedicated accounts where practical, avoid shared machines for exported cookies, and log out or clear session files when access is no longer needed. <br>
Risk: The skill starts persistent helper services for download and PO token workflows. <br>
Mitigation: Keep local services bound to localhost or protected by a firewall, and stop services when the skill is not in use. <br>
Risk: Proxy settings, tokens, or session data may be exposed through configuration or logs. <br>
Mitigation: Review logs and configuration for sensitive values, avoid disabling TLS verification, and keep proxy credentials out of shared files. <br>
Risk: The clear_database control is destructive for local task and video state. <br>
Mitigation: Confirm the target database and preserve any needed state before invoking destructive cleanup tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/esanle/bootleg-link-mcp) <br>
- [bgutil-ytdlp-pot-provider documentation](https://github.com/Brainicism/bgutil-ytdlp-pot-provider?tab=readme-ov-file#faq) <br>
- [yt-dlp PO Token Guide](https://github.com/yt-dlp/yt-dlp/wiki/PO-Token-Guide) <br>
- [yt-dlp PO Token Provider Framework](https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/extractor/youtube/pot/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, configuration, guidance] <br>
**Output Format:** [JSON-RPC tool responses with text payloads; downloaded media files are written to configured local paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates, deletes, resumes, and reports on download tasks while maintaining local SQLite state and media output.] <br>

## Skill Version(s): <br>
0.9.3 (source: server release metadata; artifact frontmatter says 0.9.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
