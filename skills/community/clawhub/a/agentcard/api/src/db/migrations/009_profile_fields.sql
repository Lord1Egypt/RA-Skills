-- Migration: Add email and phone to owner_telegram_links for profile management

ALTER TABLE owner_telegram_links
  ADD COLUMN IF NOT EXISTS email TEXT,
  ADD COLUMN IF NOT EXISTS phone TEXT;
