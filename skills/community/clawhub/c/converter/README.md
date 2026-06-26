# Converter: The Local Conversion Router (v2.0.0)

> Your information. Any realistic container. No quiet uploads.

Converter 2.0.0 moves from a magic-promise file converter to a **local-first conversion router**.

It does not pretend every format path is equally possible.  
It identifies the best local route, tells you what will be preserved or lost, and either converts locally with trusted binaries or gives you an honest fallback plan.

## Why 2.0.0

- **Engineering reality**: local tool dependencies are declared explicitly
- **Route diagnosis**: every request starts with fidelity and compatibility analysis
- **Privacy-first**: local execution by default, explicit consent before any external route
- **Honest boundaries**: no DRM bypass, no password cracking, no fake quality restoration

## Toolchain Integration

This skill acts as a logic wrapper around common local tools:

- **Pandoc** for document structure conversion
- **FFmpeg** for audio/video transcoding
- **ImageMagick** for raster image conversion
- **LibreOffice (`soffice`)** for office exports
- **7z** for archive handling

## Core Principle

A good converter should not just say “yes.”

It should say:
- what the best path is
- what will survive
- what may degrade
- whether the path is exact, lossy, reconstructed, or unsupported

## Safety

Local-first by default.  
No quiet uploads.  
No magic claims.  
Just explicit routes, explicit tradeoffs, and local toolchains you can verify.
