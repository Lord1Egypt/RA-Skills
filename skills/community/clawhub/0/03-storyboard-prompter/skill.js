module.exports = async function main({ inputs }) {
  const { scenes } = inputs;

  const shot_list = scenes.map((item, index) => {
    return {
      shot_id: index + 1,
      prompt: `${item.scene}, ${item.role}, ${item.action}, 9:16, cinematic, high detail`,
      duration: item.duration
    };
  });

  return { shot_list };
};
