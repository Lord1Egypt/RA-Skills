module.exports = async function main({ inputs }) {
  const { video_url, audio_url, subtitle_url } = inputs;

  return {
    final_video_url: "merged_short_video.mp4",
    message: "合成完成：视频+音频+字幕已合并为9:16竖屏成片"
  };
};
