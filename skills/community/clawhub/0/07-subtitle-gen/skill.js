module.exports = async function main({ inputs }) {
  const { audio_url, dialogue = "" } = inputs;

  return {
    subtitle_url: "auto_generated_subtitle.srt",
    content: "1\n00:00:00 --> 00:00:03\n" + dialogue
  };
};
