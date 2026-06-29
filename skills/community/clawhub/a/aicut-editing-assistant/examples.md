# 地鼠AI剪辑 Bridge 接口调用示例

## 1. 等待 Bridge 就绪

```js
// 方式一：Promise
const bridge = await window.aicutAIReady;

// 方式二：事件
window.addEventListener("aicutAIReady", (e) => {
	console.log("Bridge ready, version:", e.detail.version);
});

// 方式三：轮询（兜底）
while (!window.aicutAI) {
	await new Promise((r) => setTimeout(r, 200));
}
```

## 2. 获取运行时能力

```js
const caps = window.aicutAI.getCapabilities();

console.log("桌面端:", caps.desktop.isTauri ? "Tauri" : "浏览器");
console.log("推荐输入:", caps.desktop.recommendedInput);
console.log("本地媒体桥接:", caps.desktop.localMediaBridge);
console.log("音量范围:", caps.volume.min, "~", caps.volume.max, "dB");
console.log("人声推荐:", caps.volume.voiceRecommended, "dB");
console.log("BGM 推荐:", caps.volume.musicRecommended, "dB");
console.log("支持的导入方式:", caps.importMedia.supportedInputs);
console.log("大视频推荐:", caps.importMedia.recommendedForLargeVideo);
console.log(
	"字幕预设:",
	caps.subtitles.presets.map((p) => p.id),
);
```

## 2.1 AI 自动粗剪 + 审片重剪闭环

给 QwenClaw / OpenClaw / Codex 代理使用时，优先调用完整 workflow，并以
`review.qualityGate` 作为机器判断依据，而不是只读自然语言建议。

MCP/CLI 标准顺序：

```text
1. health / capabilities
2. ai_editing_preflight({folder?})，确认 Bridge、当前项目、本地素材是否就绪
3. 如果素材还没导入且 preflight 显示有视频/音频，优先用 ai_editing_from_folder({folder, goal, reviewIterations:3, applyReviewPlan:true})
4. 如果素材已导入，用 ai_editing_workflow({goal, reviewIterations:3, applyReviewPlan:true})
5. 如果 review.qualityGate.nextAction=run_revision，继续 ai_cut_review({applyRevisedPlan:true})
6. 如果 status=pass，进入导出前人工终审
7. 如果 status=human_review，停止自动重剪，要求人工确认风险
```

`ai_editing_from_folder` 会自动完成 local_media_authorize、有限扫描、筛选视频/音频/图片、
tauriPath 导入和 workflow。只有需要精细控制导入素材时，才手动调用
`local_media_authorize → local_media_list → media_import → ai_editing_workflow`。
如果 preflight 的 `recommendedNextAction=provide_video_or_audio_for_full_editing`，
说明只有图片/缩略图，不能当成完整视频剪辑验收。

如果授权的是桌面、工作区或工程根目录，先用较小的 `maxDepth/maxEntries`
做有限扫描；如果 `scan.truncated=true`，让用户授权更具体的素材文件夹。
图片/缩略图可以用 `local_media_read` 读取 base64 给多模态模型看；大视频不要
base64 读取，必须用 `local_media_list` 返回的 `entry.path` 作为 `tauriPath` 导入。

```js
const result = await window.aicutAI.runAiEditingWorkflow({
	goal: "剪成抖音纪实口播，前2秒要有冲突和结果，现场证据穿插，字幕清楚",
	script: "可选：用户确认过的口播稿或剧情主线",
	replaceTimeline: true,
	reviewIterations: 3,
	applyReviewPlan: true,
	autoPlayPreview: true,
});

const gate = result.review?.qualityGate;

if (gate?.status === "pass") {
	console.log("粗剪达标，进入导出前人工终审。");
}

if (gate?.nextAction === "run_revision") {
	console.log("仍需重剪，查看 reviewHistory 里的每轮原因。");
}

if (gate?.nextAction === "analyze_assets") {
	console.log("素材理解不足，先补跑 narration_audit / 素材分析。");
}

if (gate?.status === "human_review") {
	console.log("存在隐私/合同/后台/客户信息等风险，不要自动导出。");
}

console.log("每轮审片历史:", result.reviewHistory);
```

单独审片当前时间线时：

```js
const reviewResult = await window.aicutAI.reviewAiEditingCut({
	goal: "剪成抖音纪实口播，前2秒要有冲突和结果",
	applyRevisedPlan: true,
});

console.log(reviewResult.review.qualityGate);
console.log(reviewResult.applied);
// applied.reason:
// applied_revised_plan | apply_disabled | no_revised_plan |
// quality_gate_pass | quality_gate_human_review |
// quality_gate_requires_analysis | quality_gate_no_revision
```

## 2.2 本地精华剪辑兜底

当 HEVC/WebCodecs/浏览器预览不稳，但 AI 已经完成转写、气口判断和 B-roll 计划时，
不要停在“预览失败”。使用本地 ffmpeg 兜底命令直接导出可验收成片：

```bash
aicut local essence-cut @/absolute/path/to/local-essence-cut-plan.json \
  --output /absolute/path/to/final.mp4 \
  --report /absolute/path/to/final-report.md
```

计划模板见：

```text
apps/aicut-cli/examples/local-essence-cut-plan.json
```

同一能力也暴露给独立 MCP Server：

```text
tool: local_essence_cut
input: { "plan": { ...同一份 JSON... } }
```

如果用户反馈“某一段字幕对不上”，不要继续手调旧 SRT。先抽取最终成片音频并用 Whisper 生成 JSON/SRT，再用字幕对齐工具生成新字幕轨：

```bash
aicut local subtitle-align @/absolute/path/to/subtitle-align-plan.json \
  --transcript /absolute/path/to/final-audio-whisper.json \
  --srt-output /absolute/path/to/aligned.srt \
  --ass-output /absolute/path/to/aligned.ass \
  --report /absolute/path/to/subtitle-align-report.md \
  --check-times 8,12,16,20,24,28,32,35
```

计划模板见：

```text
apps/aicut-cli/examples/local-subtitle-align-plan.json
```

MCP 工具：

```text
tool: local_subtitle_align
input: { "plan": { "transcript": "...whisper.json", "captions": [{ "text": "...", "transcriptIndex": 0 }] } }
```

硬规则：

- `mainRanges` 只放主口播精华段，不能把空话和重复口癖全部保留。
- `voiceAudio` 必须是主口播或确认配音，不使用 B-roll 原声做主音频。
- `broll[].muted` 默认 true，本地工具只取 B-roll 画面，不混入 B-roll 声音。
- `subtitleAss` 必须来自原生口播/确认配音稿，不写 AI 剪辑思路。
- 字幕返工必须以最终成片音频时间轴为准；不要用旧人工估算时间轴覆盖。
- 导出后工具会自动检查 video/audio stream 和 `mean_volume` / `max_volume`。

## 3. 读取项目快照

```js
const snapshot = window.aicutAI.getProjectSnapshot();
console.log("项目:", snapshot.project.name);
console.log("画布:", snapshot.project.canvasSize);
console.log("时长:", snapshot.project.durationSeconds, "秒");
console.log("媒体库:", snapshot.media.length, "个素材");
console.log("主轨:", snapshot.timeline.main.length, "个片段");
console.log("音频轨:", snapshot.timeline.audio.length, "个片段");
console.log("叠加轨:", snapshot.timeline.overlay.length, "个片段");

// 媒体信息
snapshot.media.forEach((asset) => {
	console.log(
		`  ${asset.name} [${asset.type}] ${asset.durationSeconds}s ${asset.width}x${asset.height} audio:${asset.hasAudio}`,
	);
	console.log(`  fingerprint: ${asset.fingerprint}`);
});
```

## 4. 导入素材

### 4.1 数组简写

```js
// File 对象
const result = await window.aicutAI.importMedia([
	{ id: "v1", name: "clip.mp4", file: fileObject, mimeType: "video/mp4" },
]);

// Blob
const blob = new Blob([arrayBuffer], { type: "audio/m4a" });
const result = await window.aicutAI.importMedia([
	{ id: "a1", name: "voice.m4a", blob, mimeType: "audio/m4a" },
]);

// URL
const result = await window.aicutAI.importMedia([
	{ id: "m1", name: "asset.mp4", url: "https://example.com/asset.mp4" },
]);

// tauriPath（地鼠AI剪辑桌面端）
const result = await window.aicutAI.importMedia([
	{ id: "t1", name: "video.mp4", tauriPath: "/Users/user/Media/video.mp4" },
]);

// AI 代理推荐：先让桌面端授权/选择文件夹，再使用 listFolder 返回的 entry.path
const picked = await window.aicutAI.localMedia.pickFolder();
const entries = await window.aicutAI.localMedia.listFolder(picked.rootId);
const videos = entries
	.filter((entry) => entry.type === "video")
	.map((entry) => ({
		id: entry.path,
		name: entry.name,
		tauriPath: entry.path,
		mimeType: entry.mimeType,
	}));
const importedVideos = await window.aicutAI.importMedia(videos);

// localPath（需服务端路由 + AICUT_LOCAL_MEDIA_ROOTS）
const result = await window.aicutAI.importMedia([
	{
		id: "l1",
		name: "local.mp4",
		localPath: "/data/media/local.mp4",
		localMediaToken: "xxx",
	},
]);

// base64（不推荐用于大视频）
const result = await window.aicutAI.importMedia([
	{
		id: "b1",
		name: "small.jpg",
		base64: "data:image/png;base64,...",
		mimeType: "image/png",
	},
]);
```

### 4.2 带进度回调

```js
const result = await window.aicutAI.importMedia({
	media: [
		{ id: "v1", name: "clip.mp4", url: "https://example.com/clip.mp4" },
		{ id: "v2", name: "intro.mp4", url: "https://example.com/intro.mp4" },
	],
	options: {
		onProgress: (progress) => {
			console.log(`${progress.name}: ${progress.stage} ${progress.progress}%`);
			// stage: "fetching" | "processing" | "registered" | "failed"
			if (progress.bytesLoaded && progress.bytesTotal) {
				console.log(`  ${progress.bytesLoaded}/${progress.bytesTotal} bytes`);
			}
		},
		signal: abortController.signal, // 支持取消
	},
});

console.log("导入成功:", result.imported);
console.log("ID 映射:", result.idMap); // { "v1": "real-id-1", "v2": "real-id-2" }
console.log("导入失败:", result.failed); // [{ tempId, name, reason, code }]
```

### 4.3 导入结果处理

```js
// idMap 用于将临时 ID 映射到真实 mediaId
const idMap = result.idMap;

// imported 包含每个成功导入的详情
result.imported.forEach((item) => {
	console.log(
		`${item.name} → ${item.mediaId}, ${item.type}, ${item.durationSeconds}s, ${item.sourceType}`,
	);
});

// failed 包含错误码
result.failed.forEach((item) => {
	console.error(`${item.name} 失败: ${item.reason} (code: ${item.code})`);
	// code: aborted | local_path_not_supported_in_browser | fetch_401 | fetch_403 |
	//       fetch_404 | fetch_failed | unsupported_codec | unsupported_media |
	//       quota_exceeded | desktop_bridge_not_available | import_failed | missing_media_source
});
```

## 5. 排时间线

```js
const snapshot = window.aicutAI.getProjectSnapshot();
const videoId = snapshot.media[0].id;
const audioId = snapshot.media.find((m) => m.name === "voice.m4a").id;

const result = window.aicutAI.applyTimeline({
	canvasSize: { width: 1440, height: 1080 },
	clearTimeline: true,
	muteAllVideoSourceAudio: false,
	timeline: {
		main: [
			{
				mediaId: videoId,
				timelineStart: 0,
				sourceStart: 0,
				sourceEnd: 30,
				sourceAudioEnabled: true,
				volumeDb: 0,
			},
			{
				mediaId: anotherVideoId,
				timelineStart: 30,
				sourceStart: 5,
				duration: 15, // 用 duration 替代 sourceEnd
			},
		],
		audio: [
			{
				mediaId: audioId,
				timelineStart: 0,
				volumeDb: 0, // 口播正常音量
				muted: false,
			},
			{
				mediaId: bgmId,
				timelineStart: 0,
				volumeDb: -18, // BGM 低音量铺底
				muted: false,
			},
		],
	},
});

console.log("主轨插入:", result.insertedMainCount);
console.log("音频插入:", result.insertedAudioCount);
console.log("缺失媒体:", result.missingMediaIds);
```

## 6. applyProject 一步完成

```js
const result = await window.aicutAI.applyProject({
	canvasSize: { width: 1440, height: 1080 },
	clearTimeline: true,
	muteAllVideoSourceAudio: false,
	media: [
		{ id: "v1", name: "clip.mp4", file: fileObject, mimeType: "video/mp4" },
		{ id: "a1", name: "voice.m4a", file: audioFile, mimeType: "audio/m4a" },
	],
	timeline: {
		main: [{ mediaId: "v1", timelineStart: 0, sourceStart: 0, sourceEnd: 60 }],
		audio: [{ mediaId: "a1", timelineStart: 0, volumeDb: 0 }],
	},
	captions: [
		{
			text: "第一句字幕",
			startTime: 0,
			duration: 4,
			style: { preset: "douyinSafe" },
		},
		{ text: "第二句字幕", startTime: 4.5, duration: 3.5 },
	],
	subtitleStyle: { preset: "douyinSafe" }, // 全局字幕样式
});

console.log("媒体导入:", result.media.imported.length, "成功");
console.log("主轨:", result.timeline.insertedMainCount);
console.log("字幕轨:", result.captionTrackId);
console.log("项目快照:", result.project);
```

## 7. 导入字幕

### 7.1 SRT 导入

```js
const srtText = `1
00:00:01,000 --> 00:00:04,000
第一句字幕内容

2
00:00:04,500 --> 00:00:08,000
第二句字幕内容
`;

const result = window.aicutAI.importSrt({
	srtText,
	fileName: "captions.srt", // 可选
	style: { preset: "douyinSafe" },
});

console.log("字幕轨:", result.trackId);
console.log("插入条数:", result.insertedCount);
console.log("警告:", result.warnings);
```

### 7.2 直接 captions（applyProject 内）

```js
// 更灵活，每条字幕可独立设置样式
applyProject({
	captions: [
		{
			text: "开头字幕",
			startTime: 0,
			duration: 2,
			style: { preset: "douyinSafe" },
		},
		{
			text: "重点内容",
			start: 2,
			duration: 3,
			style: { preset: "douyinSafe", fontWeight: "bold" },
		},
	],
	subtitleStyle: { preset: "douyinSafe" }, // 全局默认，单条 style 可覆盖
});
```

### 7.3 SRT + captions 混合

```js
// applyProject 中 srtText 和 captions 可同时使用，会合并
applyProject({
	captions: [{ text: "自定义开头", startTime: 0, duration: 2 }],
	srtText: srtContent,
	srtFileName: "captions.srt",
	subtitleStyle: { preset: "douyinSafe" },
});
```

## 8. 导出前校验

```js
const validation = window.aicutAI.validateProject();
console.log("校验结果:", validation);

// 检查关键项
if (validation.durationSeconds <= 0) {
	console.error("项目时长为零！");
}
if (validation.mainTrackCount === 0) {
	console.error("主轨没有片段！");
}
if (validation.allVideoSourceAudioMuted === false) {
	console.warn("视频原声未全部关闭！");
}
if (validation.missingMedia.length > 0) {
	console.error("缺失媒体:", validation.missingMedia);
}
if (validation.subtitleCount === 0) {
	console.warn("没有字幕！");
}
console.log("警告:", validation.warnings);
```

## 9. 播放控制

```js
const player = window.aicutAI.player;

// 播放/暂停
player.play();
player.pause();

// 跳转到关键位置
player.seek(15.5);

// 获取状态
const state = player.getState();
console.log("播放中:", state.isPlaying);
console.log("静音:", state.isMuted);
console.log("音量:", state.volume);
console.log("当前时间:", state.currentTimeSeconds);
console.log("总时长:", state.totalDurationSeconds);

// 事件监听（旧 API）
player.onUpdate((state) => console.log("时间更新:", state.currentTimeSeconds));
player.onSeek((state) => console.log("跳转:", state.currentTimeSeconds));
player.onEnded((state) => console.log("播放结束"));

// 事件监听（统一 API）
player.on({
	event: "timeupdate",
	listener: (state) => console.log("更新:", state.currentTimeSeconds),
});
player.on({ event: "seek", listener: (state) => console.log("跳转") });
player.on({ event: "ended", listener: (state) => console.log("结束") });
player.on({
	event: "statechange",
	listener: (state) => console.log("状态变化"),
});

// subscribe（alias for onUpdate）
const unsubscribe = player.subscribe((state) =>
	console.log("时间:", state.currentTimeSeconds),
);
// 取消监听
unsubscribe();
```

## 10. 项目事件监听

```js
// 方式一：bridge.on（推荐）
const off1 = window.aicutAI.on({
	event: "ready",
	listener: (payload) => console.log("Bridge 就绪:", payload.project.name),
});
const off2 = window.aicutAI.on({
	event: "projectChanged",
	listener: (payload) => console.log("项目切换:", payload.project.name),
});
const off3 = window.aicutAI.on({
	event: "projectLoaded",
	listener: (payload) => console.log("项目加载:", payload.project.name),
});

// 取消监听
off1();
off2();
off3();

// 方式二：DOM 事件
window.addEventListener("aicutAI:ready", (e) => console.log("就绪", e.detail));
window.addEventListener("aicutAI:projectChanged", (e) =>
	console.log("切换", e.detail),
);
window.addEventListener("aicutAI:projectLoaded", (e) =>
	console.log("加载", e.detail),
);
```

## 11. 项目生命周期

```js
// 新建项目
const project = await window.aicutAI.createProject({ name: "测试项目" });
console.log("项目 ID:", project.id);
console.log("项目名:", project.name);
console.log("时长:", project.durationSeconds, "秒");
console.log("创建时间:", project.createdAt);

// 列出项目
const projects = await window.aicutAI.listProjects();
projects.forEach((p) =>
	console.log(`${p.id} ${p.name} ${p.isCurrent ? "← 当前" : ""}`),
);

// 打开项目
await window.aicutAI.openProject({ id: "project-id" });

// 当前项目
const current = window.aicutAI.getCurrentProject();
```

## 12. 桌面端本地文件桥接

```js
const localMedia = window.aicutAI.localMedia;

// 检查可用性
if (!localMedia.isAvailable()) {
	console.log("桌面端本地桥接不可用（需 地鼠AI剪辑桌面端）");
	return;
}

// 桌面端信息
const info = await localMedia.desktopInfo();
console.log("平台:", info.platform, "版本:", info.version);

// 选择文件夹（弹出对话框）
const listing = await localMedia.pickFolder();
console.log("根目录:", listing.root);
listing.entries.forEach((entry) => {
	console.log(
		`  ${entry.name} [${entry.type}] ${entry.size} bytes ${entry.extension}`,
	);
	// entry.type: "video" | "audio" | "image" | "subtitle"
});

// 授权文件夹
await localMedia.authorizeFolder("/path/to/media");

// 列出文件夹
const files = await localMedia.listFolder("/path/to/media");

// 获取已授权根目录
const roots = await localMedia.getAuthorizedRoots();
roots.forEach((r) => console.log("已授权:", r.path));

// 撤销授权
await localMedia.revokeRoots();

// 读取文件（base64）
const file = await localMedia.readFile("/path/to/video.mp4");
console.log("文件:", file.name, file.mimeType, file.size, "bytes");

// 转为 importMedia 输入
const inputs = localMedia.toImportMedia(listing);
// 或带字幕
const inputs = localMedia.toImportMedia({
	listing,
	options: { includeSubtitles: true },
});
await window.aicutAI.importMedia(inputs);
```

## 13. 关闭所有视频原声

```js
const result = window.aicutAI.muteAllVideoSourceAudio();
console.log("已关闭", result.updatedCount, "个视频片段的原声");
```

## 14. 导出

```js
const result = await window.aicutAI.exportProject({
	options: {
		format: "mp4", // "mp4" | "webm"
		quality: "high", // "low" | "medium" | "high" | "very_high"
		fps: 30, // 可选帧率
		includeAudio: true, // 是否包含音频（默认 true）
	},
	download: true, // 自动下载（默认 true）
});

if (result.success) {
	console.log("导出成功:", result.filename);
	if (result.downloaded) {
		console.log("已自动下载");
	}
} else if (result.cancelled) {
	console.log("导出已取消");
} else {
	console.error("导出失败:", result.error);
}

// 不自动下载，获取 buffer
const result = await window.aicutAI.exportProject({
	options: { format: "mp4", quality: "high" },
	download: false,
});
if (result.success && result.buffer) {
	console.log("导出 buffer 大小:", result.buffer.byteLength);
}
```

## 15. 完整工作流示例

```js
// 1. 等待 Bridge
const bridge = await window.aicutAIReady;

// 2. 获取能力
const caps = bridge.getCapabilities();
console.log("运行环境:", caps.desktop.isTauri ? "桌面端" : "浏览器");

// 3. 创建项目
const project = await bridge.createProject({ name: "AI 剪辑测试" });

// 4. 导入素材
const mediaResult = await bridge.importMedia({
	media: [
		{
			id: "voiceover",
			name: "口播.m4a",
			file: audioFile,
			mimeType: "audio/m4a",
		},
		{
			id: "footage1",
			name: "现场.mp4",
			file: videoFile,
			mimeType: "video/mp4",
		},
	],
	options: {
		onProgress: (p) => console.log(`${p.name}: ${p.stage} ${p.progress}%`),
	},
});
const voiceId = mediaResult.idMap["voiceover"];
const footageId = mediaResult.idMap["footage1"];

// 5. 排时间线
bridge.applyTimeline({
	canvasSize: { width: 1440, height: 1080 },
	clearTimeline: true,
	muteAllVideoSourceAudio: false,
	timeline: {
		main: [
			{
				mediaId: footageId,
				timelineStart: 0,
				sourceStart: 0,
				sourceEnd: 60,
				sourceAudioEnabled: false,
				muted: true,
			},
		],
		audio: [{ mediaId: voiceId, timelineStart: 0, volumeDb: 0 }],
	},
});

// 6. 导入字幕
bridge.importSrt({ srtText: srtContent, style: { preset: "douyinSafe" } });

// 7. 校验
const validation = bridge.validateProject();
if (validation.warnings.length > 0) {
	console.warn("校验警告:", validation.warnings);
}

// 8. 预览
bridge.player.seek(0);
bridge.player.play();

// 9. 导出
const exportResult = await bridge.exportProject({
	options: { format: "mp4", quality: "high" },
	download: true,
});
console.log("导出:", exportResult.success ? "成功" : "失败");
```

## 16. CLI 使用示例

```bash
# 检查 地鼠AI剪辑 服务连接
aicut health

# 列出所有剪辑任务
aicut jobs list

# 按客户端过滤
aicut jobs list --clientId my-project

# 创建剪辑任务（内联 JSON）
aicut jobs create '{"clientId":"demo","title":"测试剪辑","goal":"自动粗剪"}'

# 创建剪辑任务（从文件读取）
aicut jobs create @job-input.json

# 查看任务详情
aicut jobs get job_abc123

# 提交素材摘要
aicut jobs summaries job_abc123 '[{"id":"a1","name":"clip.mp4","type":"video","durationSeconds":30}]'

# 更新任务状态
aicut jobs update job_abc123 '{"status":"completed","message":"审片完成"}'

# 实时监听任务（WebSocket）
aicut jobs watch --clientId demo

# 获取本地媒体 URL
aicut media url "/data/media/video.mp4"

# 下载本地媒体文件
aicut media fetch "/data/media/video.mp4" ./downloaded.mp4

# 校验 Skill JSON
aicut skill validate @skill.json

# 计算 Skill 完整度评分
aicut skill completeness @skill.json

# 输出纪实口播 Skill 模板
aicut skill template > my-skill.json
```

## 17. MCP Server 使用示例（AI 代理调用）

地鼠AI剪辑桌面端 内嵌 MCP WebSocket Server（端口 4890），AI 代理可直接连接操控。

```python
# Python 示例：通过 MCP 自动剪辑
import asyncio, websockets, json

async def auto_edit():
    uri = 'ws://localhost:4890/mcp'
    async with websockets.connect(uri) as ws:
        # 1. 初始化
        await ws.send(json.dumps({
            'jsonrpc': '2.0', 'id': 1,
            'method': 'initialize',
            'params': {'protocolVersion': '2024-11-05', 'capabilities': {},
                       'clientInfo': {'name': 'ai-agent', 'version': '1.0'}}
        }))
        r = json.loads(await ws.recv())
        print(f"Connected: {r['result']['serverInfo']}")

        # 2. 授权文件夹
        await ws.send(json.dumps({
            'jsonrpc': '2.0', 'id': 10,
            'method': 'tools/call',
            'params': {'name': 'bridge_call',
                       'arguments': {'method': 'localMedia.authorizeFolder',
                                     'args': {'path': '/Users/user/Desktop'}}}
        }))
        await ws.recv()

        # 3. 一步完成：导入+排时间线+字幕+关原声
        await ws.send(json.dumps({
            'jsonrpc': '2.0', 'id': 20,
            'method': 'tools/call',
            'params': {'name': 'project_apply',
                       'arguments': {
                           'canvasSize': {'width': 1440, 'height': 1080},
                           'clearTimeline': True,
                           'muteAllVideoSourceAudio': True,
                           'media': [{'id': 'v1', 'name': 'clip.mp4',
                                      'tauriPath': '/Users/user/Desktop/clip.mp4'}],
                           'timeline': {'main': [{'mediaId': 'v1', 'timelineStart': 0}]},
                           'captions': [{'text': 'AI 自动剪辑', 'startTime': 0,
                                         'duration': 5, 'style': {'preset': 'douyinSafe'}}],
                           'subtitleStyle': {'preset': 'douyinSafe'}
                       }}
        }))
        r = json.loads(await ws.recv())
        print(f"Apply: {r['result']['content'][0]['text'][:80]}")

        # 4. 校验
        await ws.send(json.dumps({
            'jsonrpc': '2.0', 'id': 30,
            'method': 'tools/call',
            'params': {'name': 'project_validate', 'arguments': {}}
        }))
        await ws.recv()

        # 5. 导出
        await ws.send(json.dumps({
            'jsonrpc': '2.0', 'id': 40,
            'method': 'tools/call',
            'params': {'name': 'project_export',
                       'arguments': {'format': 'mp4', 'quality': 'high', 'download': True}}
        }))
        r = json.loads(await ws.recv())
        print(f"Export done!")

asyncio.run(auto_edit())
```

### 通用 MCP Tool 调用格式

```json
// 检查服务
{ "method": "tools/call", "params": { "name": "health", "arguments": {} } }

// 项目快照
{ "method": "tools/call", "params": { "name": "project_snapshot", "arguments": {} } }

// 通用 Bridge 调用（可调任意 window.aicutAI 方法）
{
  "method": "tools/call",
  "params": {
    "name": "bridge_call",
    "arguments": { "method": "localMedia.getAuthorizedRoots", "args": {} }
  }
}

// 导出视频（获取 buffer）
{
  "method": "tools/call",
  "params": {
    "name": "project_export",
    "arguments": { "format": "mp4", "quality": "high", "download": false }
  }
}
```
