#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    cli::agent_review::run().await
}
