# Install ctyun-cli

`ctyun-cli` is required. Without it, do not query, analyze, or check bills. Use the official installation guide: <https://www.ctyun.cn/document/11095072/11096343>.

The agent may install `ctyun-cli` with an official method only when the user asks or approves. First check the OS and CPU. Use only the official one-click installer or setup package. Do not use `pip`, `npm`, Homebrew, source builds, or third-party download sites. Tell the user that installation writes to the user directory and PATH.

Verify installation with:

```text
ctyun-cli version
ctyun-cli --help
```

After verification, **the user must personally run `ctyun-cli configure`** in their own terminal. The agent **must not run it, type values into it, or receive** AccessKey or SecretKey. Do not continue until local setup and required permission are ready.
