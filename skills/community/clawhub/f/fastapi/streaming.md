# Streaming, Uploads, and Downloads — Data Bigger Than Memory

The rule that decides everything here: a normal response is built entirely in memory before the first byte leaves. Anything whose size scales with the data must stream, or the worker's memory scales with it too.

## Uploads

| Declaration | Behavior |
|---|---|
| `file: Annotated[UploadFile, File()]` | Spooled: kept in memory up to 1 MB, then written to a temporary file on disk |
| `data: Annotated[bytes, File()]` | Whole file loaded into memory as bytes — never for user-supplied sizes |
| `request.stream()` | Raw chunks, no buffering, no multipart parsing — you handle the framing |

- `python-multipart` must be installed or every form and upload route fails at import.
- Read in chunks and never `await file.read()` without a size on an untrusted upload:

```python
CHUNK = 1024 * 1024
total = 0
while chunk := await file.read(CHUNK):
    total += len(chunk)
    if total > MAX_UPLOAD_BYTES:
        raise HTTPException(413, "File too large")
    await out.write(chunk)
```

- FastAPI enforces no maximum body size. The real limit is whatever sits in front: nginx's `client_max_body_size` defaults to 1 MB and returns 413 before your handler runs (`deployment.md`). Set both — the proxy for protection, the app for a decent error message.
- `UploadFile.file` is a synchronous file object; writing it out with blocking I/O inside `async def` blocks the loop for the whole file. Use the async methods, or a `def` endpoint (`async.md`).
- Validate content by inspecting the first bytes, not by trusting `content_type` or the filename extension; sanitize the filename before it ever reaches a path (`Path(name).name`, then your own generated key).
- Large user uploads that go to object storage should skip the app entirely: issue a presigned URL and let the client upload directly. The app's job becomes issuing the URL and recording the result.

## Downloads

```python
return FileResponse(path, filename="report.csv", media_type="text/csv")
```

- `FileResponse` streams from disk, sets `Content-Length`, and supports range requests — always better than reading a file into memory.
- Generated content streams from a generator:

```python
async def rows():
    yield "id,name\n"
    async for r in repo.iter_rows():
        yield f"{r.id},{r.name}\n"
return StreamingResponse(rows(), media_type="text/csv",
                         headers={"Content-Disposition": 'attachment; filename="rows.csv"'})
```

- A sync generator passed to `StreamingResponse` is iterated in the threadpool, consuming a slot for the whole download (SKILL.md rule 2). A slow client on a large file holds that slot for minutes.
- No `Content-Length` on a streamed response means the client sees a chunked transfer and cannot show progress. Set it when you know the size.
- Database cursors inside a streaming generator hold a connection for the entire download; for large exports, either accept that (and size the pool for it) or write to object storage and return a link.
- The status code is committed with the first byte: an error raised mid-stream can only truncate the response or emit an in-band error record (`errors.md`).

## Server-Sent Events

```python
async def events():
    while True:
        if await request.is_disconnected(): break
        yield f"event: update\ndata: {json.dumps(payload)}\n\n"
        await asyncio.sleep(15)          # or a heartbeat: ": ping\n\n"
return StreamingResponse(events(), media_type="text/event-stream",
                         headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
```

- Wire format is exact: `data:` lines, a blank line to terminate an event, `\n\n` endings. One missing newline and the browser buffers forever.
- Buffering proxies are the number one SSE bug: nginx buffers by default, so nothing reaches the client until the stream ends. `X-Accel-Buffering: no` disables it for nginx; other proxies need their own setting.
- Send a comment heartbeat (`: ping`) below every idle-timeout in the path (proxy, load balancer, browser) or the connection dies silently.
- Each open stream holds a worker's connection slot; N concurrent listeners is N connections per worker. Beyond a few thousand, or when clients must also send messages, use WebSockets (`websockets.md`).
- `id:` fields plus honoring `Last-Event-ID` on reconnect turn a dropped connection into a resumable one instead of a gap.

## Streaming Through Middleware

`BaseHTTPMiddleware` passes the body through an internal queue and loses backpressure, so a large stream can be buffered in memory (`middleware.md`). Streaming routes need pure ASGI middleware or none.

## Proxying An Upstream Stream

```python
async def proxy():
    async with client.stream("GET", url) as r:
        async for chunk in r.aiter_bytes():
            yield chunk
```

Do not `await client.get(url)` and forward `.content`: that materializes the whole upstream body in the worker first, doubling memory and adding the full download to time-to-first-byte.

## Choosing The Transport

| Need | Use |
|---|---|
| Big file to or from disk/storage | `FileResponse`, presigned URL, or chunked upload |
| Rows generated as they are read | `StreamingResponse` with a generator |
| Server pushes updates, client only listens | SSE — plain HTTP, reconnects for free |
| Both directions, low latency | WebSocket (`websockets.md`) |
| Result available later, no live channel | 202 plus a status endpoint (`background.md`) |
