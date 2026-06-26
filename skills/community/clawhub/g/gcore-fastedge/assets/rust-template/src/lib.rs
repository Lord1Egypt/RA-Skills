use fastedge::{
    body::Body,
    http::{Request, Response, StatusCode, Error},
};

#[fastedge::http]
fn main(_req: Request<Body>) -> Result<Response<Body>, Error> {
    Response::builder()
        .status(StatusCode::OK)
        .header("content-type", "text/html; charset=utf-8")
        .body(Body::from(r#"<!DOCTYPE html>
<html><head><title>FastEdge App</title></head>
<body><h1>Hello from FastEdge!</h1></body>
</html>
"#))
}
