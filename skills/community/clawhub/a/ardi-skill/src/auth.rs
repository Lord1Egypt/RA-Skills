// Resolve agent address — strictly via awp-wallet.
//
// We don't accept env-supplied addresses here because the address must
// match the key we'll sign with, and the key always comes from awp-wallet.
// Letting an env override the address opens a footgun where a user types
// commands as one address but signs with another.

use anyhow::{anyhow, Result};

use crate::wallet::WalletStatus;

pub fn get_address() -> Result<String> {
    let s = WalletStatus::check();
    s.address
        .ok_or_else(|| anyhow!("could not determine agent address: {}", s.human_status))
}
