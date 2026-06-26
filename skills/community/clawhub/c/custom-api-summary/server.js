import express from "express";

const app = express();
app.use(express.json());

// 👉 Skill 接口 - 接收用户输入并转发到目标 API
app.post("/api/skill/call", async (req, res) => {
  const { content } = req.body;

  if (!content) {
    return res.json({
      success: false,
      message: "content 不能为空"
    });
  }

  try {
    console.log("收到用户输入:", content);
    console.log("正在调用目标 API...");

    // 👉 调用目标 API
    const response = await fetch("https://test-gig-c-api.1haozc.com/api/wx/kjj/v1/customer/skill/call", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ content })
    });

    const data = await response.json();
    console.log("目标 API 返回:", data);

    // 返回目标 API 的结果给用户
    res.json({
      success: true,
      result: data
    });
  } catch (error) {
    console.error("API 调用失败:", error);
    res.json({
      success: false,
      message: "调用 API 失败: " + error.message
    });
  }
});

// 健康检查接口
app.get("/health", (req, res) => {
  res.json({ status: "ok" });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Skill API running on port ${PORT}`);
});