export default async function run(input) {
  // 1. 提取 BV号
  const match = input.match(/BV[a-zA-Z0-9]+/);
  if (!match) {
    return { error: "未找到 BV 号" };
  }

  const bvid = match[0];

  // 2. 调 B站官方 API
  const res = await fetch(
    `https://api.bilibili.com/x/web-interface/view?bvid=${bvid}`,
    {
      headers: {
        "User-Agent": "Mozilla/5.0"
      }
    }
  );

  const json = await res.json();

  if (json.code !== 0) {
    return { error: "API 返回异常" };
  }

  const d = json.data;

  // 3. 返回结构化数据
  return {
    title: d.title,
    up: d.owner.name,
    desc: d.desc,
    view: d.stat.view,
    like: d.stat.like
  };
}