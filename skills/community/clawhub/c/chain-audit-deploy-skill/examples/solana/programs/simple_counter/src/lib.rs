use anchor_lang::prelude::*;

declare_id!("11111111111111111111111111111111");

/// A minimal Solana Anchor counter program for audit demonstration.
/// Demonstrates: account validation, PDA, signer checks, events.
#[program]
pub mod simple_counter {
    use super::*;

    /// Initialize a new counter account.
    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        let counter = &mut ctx.accounts.counter;
        counter.authority = ctx.accounts.authority.key();
        counter.value = 0;
        counter.bump = ctx.bumps.counter;

        emit!(CounterChanged {
            authority: counter.authority,
            value: 0,
        });

        Ok(())
    }

    /// Increment the counter by 1. Anyone can call.
    pub fn increment(ctx: Context<Increment>) -> Result<()> {
        let counter = &mut ctx.accounts.counter;
        counter.value = counter
            .value
            .checked_add(1)
            .ok_or(ErrorCode::Overflow)?;

        emit!(CounterChanged {
            authority: counter.authority,
            value: counter.value,
        });

        Ok(())
    }

    /// Reset the counter to 0. Only the authority can call.
    pub fn reset(ctx: Context<Reset>) -> Result<()> {
        let counter = &mut ctx.accounts.counter;
        counter.value = 0;

        emit!(CounterChanged {
            authority: counter.authority,
            value: 0,
        });

        Ok(())
    }
}

// ======== Accounts ========

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        init,
        payer = authority,
        space = 8 + Counter::INIT_SPACE,
        seeds = [b"counter", authority.key().as_ref()],
        bump,
    )]
    pub counter: Account<'info, Counter>,

    #[account(mut)]
    pub authority: Signer<'info>,

    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct Increment<'info> {
    #[account(mut)]
    pub counter: Account<'info, Counter>,
}

#[derive(Accounts)]
pub struct Reset<'info> {
    #[account(
        mut,
        has_one = authority,
    )]
    pub counter: Account<'info, Counter>,

    pub authority: Signer<'info>,
}

// ======== State ========

#[account]
#[derive(InitSpace)]
pub struct Counter {
    pub authority: Pubkey,
    pub value: u64,
    pub bump: u8,
}

// ======== Events ========

#[event]
pub struct CounterChanged {
    pub authority: Pubkey,
    pub value: u64,
}

// ======== Errors ========

#[error_code]
pub enum ErrorCode {
    #[msg("Counter overflow")]
    Overflow,
}
