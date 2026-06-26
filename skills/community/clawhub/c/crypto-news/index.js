// index.js
// 1. 严格读取环境变量中的 API Key
const apiKey = process.env.BLOCKBEATS_API_KEY;

// 2. 强制拦截：如果没有配置 Key，直接报错并退出
if (!apiKey) {
    console.error("❌ 缺少凭证: 无法获取快讯。请务必先在 OpenClaw 的环境变量或 .env 文件中配置 BLOCKBEATS_API_KEY。");
    process.exit(1); // 抛出异常退出码，让 AI 知道脚本执行失败了
}

// 3. 读取大模型通过环境变量传进来的参数
const size = process.env.NEWS_SIZE || '10';
const page = process.env.NEWS_PAGE || '1';
const type = process.env.NEWS_TYPE || '';

const url = `https://api.theblockbeats.news/v1/open-api/open-flash?size=${size}&page=${page}&type=${type}`;

// 4. 发起真实请求
fetch(url, {
    headers: { 'Authorization': `Bearer ${apiKey}` }
})
.then(res => res.json())
.then(data => {
    if (data?.data?.data?.length > 0) {
        const newsList = data.data.data.map(item => {
            const time = new Date(item.add_time * 1000).toLocaleString();
            return `### ${item.title}\n> 🕒 时间: ${time}\n\n${item.content}`;
        });
        // 直接打印 Markdown，OpenClaw 会截获这个输出发给用户
        console.log(newsList.join('\n\n---\n\n'));
    } else {
        console.log("未获取到相关的快讯数据。");
    }
})
.catch(err => {
    // 捕获网络异常等情况
    console.error("API 接口请求失败:", err.message);
    process.exit(1);
});