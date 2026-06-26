const express = require("express");
const app = express();

app.use(express.json());

app.post("/echo", (req, res) => {
  const { content } = req.body;

  console.log("Received:", content);

  if (!content) {
    return res.status(400).json({
      error: "content is required"
    });
  }

  res.json({
    message: `Echo: ${content}`
  });
});

const PORT = 8080;

app.listen(PORT, () => {
  console.log(`Skill server running on port ${PORT}`);
});