const EASYALPHA_API_KEY = process.env.EASYALPHA_API_KEY;

if (!EASYALPHA_API_KEY) {
    throw new Error("EASYALPHA_API_KEY environment variable is not set");
}

/**
 * 分析题材/新闻以进行股票选择 (Analysis query)
 * @param {Object} request - 请求对象
 * @param {string} request.query - 分析查询
 * @param {string} [request.type="deep"] - 分析深度 ("fast" 或 "deep")
 * @returns {AsyncGenerator<string, void, void>}
 */
async function* get_content_stock(request) {
    const url = "http://[IP_ADDRESS]/api/v1/alpha/content_stock";
    const headers = {
        "Authorization": `Bearer ${EASYALPHA_API_KEY}`,
        "Content-Type": "application/json"
    };
    const payload = {
        query: request.query,
        type: request.type || "deep"
    };

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: headers,
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            yield `data: Error: ${response.status}\n\n`;
            return;
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            yield decoder.decode(value, { stream: true });
        }
    } catch (error) {
        yield `data: Error: ${error.message}\n\n`;
    }
}

module.exports = { get_content_stock };
