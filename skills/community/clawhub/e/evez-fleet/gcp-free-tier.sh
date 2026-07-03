#!/bin/bash
# GCP Free Tier Infrastructure Setup
# Creates the always-free resources + useful paid-but-cheap ones
# Prerequisites: gcloud CLI installed and authenticated

set -euo pipefail

PROJECT="${1:?Usage: $0 <gcp-project-id>}"
REGION_US="us-west1"
REGION_CENTRAL="us-central1"

echo "🏗️ Setting up GCP free-tier infrastructure for project: $PROJECT"
gcloud config set project "$PROJECT"

# 1. Always-free e2-micro in us-west1/us-central1/us-east1
echo "=== Creating free e2-micro (us-west1) ==="
gcloud compute instances create openclaw-free \
  --zone=us-west1-b \
  --machine-type=e2-micro \
  --image-family=ubuntu-2404-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=30GB \
  --boot-disk-type=pd-standard \
  --network-tier=PREMIUM \
  2>&1 || echo "Instance may already exist"

# 2. Free Cloud Scheduler jobs (3 free)
echo "=== Setting up free Cloud Scheduler ==="
gcloud services enable cloudscheduler.googleapis.com 2>&1 | tail -1

# 3. Free Pub/Sub (10GB/month)
echo "=== Creating Pub/Sub topic for mesh communication ==="
gcloud pubsub topics create openclaw-mesh-events 2>&1 || echo "Topic exists"
gcloud pubsub subscriptions create openclaw-mesh-sub --topic=openclaw-mesh-events 2>&1 || echo "Sub exists"

# 4. Install OpenClaw on the free instance
echo "=== Installing OpenClaw on free node ==="
gcloud compute ssh openclaw-free --zone=us-west1-b --command="
  curl -fsSL https://openclaw.ai/install.sh | bash
  openclaw setup
" 2>&1 | tail -5

echo ""
echo "✅ Free-tier infrastructure created!"
echo "   - e2-micro (FREE): openclaw-free in us-west1-b"
echo "   - Pub/Sub topic: openclaw-mesh-events (FREE up to 10GB/mo)"
echo "   - Cloud Scheduler: available (3 free jobs)"
echo ""
echo "💰 Estimated monthly cost: \$0.00"
echo "   (e2-micro + 30GB standard disk + 1GB egress = all free tier)"
