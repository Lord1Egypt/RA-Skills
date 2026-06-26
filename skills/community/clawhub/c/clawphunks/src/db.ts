/**
 * Database layer for ClawPhunks
 * Uses Supabase - items table with pre-built data URIs
 */

import { createClient, SupabaseClient } from '@supabase/supabase-js';

let supabase: SupabaseClient | null = null;

function getSupabase(): SupabaseClient {
  if (supabase) return supabase;

  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_KEY;

  if (!url || !key) {
    throw new Error('SUPABASE_URL and SUPABASE_SERVICE_KEY required');
  }

  supabase = createClient(url, key);
  return supabase;
}

export interface ClaimResult {
  tokenId: number;
  dataURI: string;
}

/**
 * Claim a random unminted item for minting
 */
export async function claimRandomItem(recipient: string): Promise<ClaimResult> {
  const db = getSupabase();

  const { data, error } = await db.rpc('claim_random_item', {
    recipient: recipient.toLowerCase(),
  });

  if (error) {
    throw new Error(error.message);
  }

  if (!data || data.length === 0) {
    throw new Error('No items available');
  }

  return {
    tokenId: data[0].token_id,
    dataURI: data[0].data_uri,
  };
}

/**
 * Finalize mint with tx hash
 */
export async function finalizeMint(tokenId: number, txHash: string): Promise<void> {
  const db = getSupabase();

  const { error } = await db.rpc('finalize_mint', {
    p_token_id: tokenId,
    p_tx_hash: txHash,
  });

  if (error) {
    throw new Error(error.message);
  }
}

/**
 * Rollback a failed mint - mark item as unminted
 */
export async function rollbackMint(tokenId: number): Promise<void> {
  const db = getSupabase();

  await db
    .from('items')
    .update({ minted: false, minted_to: null, minted_at: null })
    .eq('token_id', tokenId);
}

/**
 * Get count of minted items
 */
export async function getMintedCount(): Promise<number> {
  const db = getSupabase();

  const { count, error } = await db
    .from('items')
    .select('*', { count: 'exact', head: true })
    .eq('minted', true);

  if (error) {
    throw new Error(error.message);
  }

  return count ?? 0;
}

/**
 * Get count of available (unminted) items
 */
export async function getAvailableCount(): Promise<number> {
  const db = getSupabase();

  const { count, error } = await db
    .from('items')
    .select('*', { count: 'exact', head: true })
    .eq('minted', false);

  if (error) {
    throw new Error(error.message);
  }

  return count ?? 0;
}
