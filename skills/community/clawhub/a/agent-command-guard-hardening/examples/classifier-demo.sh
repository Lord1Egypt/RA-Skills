#!/usr/bin/env bash
# Toy classifier for the example matrix. Contract: argv -> allow|deny on stdout.
bin="$1"; shift || true
case "$bin" in
  rm|sudo|dd) echo deny; exit 0 ;;
  chmod)
    for a in "$@"; do
      case "$a" in -R|-r|777) echo deny; exit 0 ;; esac
    done
    echo allow; exit 0 ;;
  *) echo allow; exit 0 ;;
esac
