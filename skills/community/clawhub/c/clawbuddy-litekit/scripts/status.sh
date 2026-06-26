#!/usr/bin/env bash
# Checks whether the deployed ClawBuddy instance has OpenClaw Gateway secrets configured.
set -euo pipefail

PROJECT_REF="ikpzzbbcxandgrzygyod"
ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlrcHp6YmJjeGFuZGdyenlneW9kIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk3MTg0NTcsImV4cCI6MjA5NTI5NDQ1N30.ZUfWeKv_kjC0AHTFI6DOVhal23e-jntRtNIooxOGjE8"

curl -s "https://${PROJECT_REF}.functions.supabase.co/openclaw-status" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ANON_KEY"
echo
