MIT License

Copyright (c) 2026 三剪客

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 使用提示

本 Skill 通过算力集市 [api.a7w.cn](https://api.a7w.cn/) 的 HTTP 接口调用 AI 能力。

- **需要使用者自己的 API Key**，本包不内嵌任何密钥
- 调用会消耗 Key 所属账号的点数/算力，具体计费以响应里的 `usage.points_cost` 与站内为准
- 生成内容的版权与合规责任由使用者承担

### ⚠️ 数字人涉及人格权，不只是版权

版权可以约定，**人格权（肖像权、声音权）只能取得本人授权，不可转让**。

- `lipsync` 与 `make` 子命令**必须**显式传 `--authorized`，否则直接拒绝执行（退出码 7）
- 剪辑类命令默认开启 AI 生成标识，**关掉之前请先确认你所在地区的标识要求**
- **未获授权的人像与声音不要使用**，也不要用明星、公众人物或来源不明的网络图片

详见 `references/通用说明.md`。

### 关于转授权

若要向客户转授权（再许可），请先确认上游条款是否允许，
并在授权书中写明「**仅授予使用许可，不构成任何上游权利的转让、担保或承诺**」
与「**非排他、非独占**」。

### 关于素材来源

本包只负责把 URL 交给平台。**素材的获取方式与其合法性由使用者负责** ——
包括但不限于：是否获得出镜人授权、是否使用了他人享有著作权的音乐与影像、
是否符合各内容平台的投放规则。
