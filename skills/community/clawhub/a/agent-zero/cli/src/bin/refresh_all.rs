#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    cli::refresh_all::run().await
}
