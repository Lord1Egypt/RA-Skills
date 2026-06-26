#!/bin/bash
# ClawHub Publish Script for OpenClaw Skills

SKILL_DIR=$1
SLUG=${2:-$(basename $SKILL_DIR)}
NAME=${3:-$SLUG}
VERSION=${4:-1.0.0}
CHANGELOG=${5:-\"Quick publish\"}

if [ -z \"$SKILL_DIR\" ]; then
  echo \"Usage: $0 <skill-dir> [slug] [name] [version] [changelog]\"
  exit 1
fi

cd $SKILL_DIR
clawhub publish . --slug $SLUG --name \"$NAME\" --version $VERSION --changelog \"$CHANGELOG\"

echo \"Published $SLUG@$VERSION 🎉\"