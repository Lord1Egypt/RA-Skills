#!/bin/bash

# Build script for Classical Chinese Translator skill package

set -e

SKILL_NAME="classical-chinese-translator"
VERSION="1.0.0"
OUTPUT_DIR="dist"
PACKAGE_NAME="${SKILL_NAME}-${VERSION}.tar.gz"

echo "Building ${SKILL_NAME} v${VERSION}..."

# Create dist directory
mkdir -p ${OUTPUT_DIR}

# Create package structure
TEMP_DIR=$(mktemp -d)
cp -r SKILL.md scripts references package.json README.md LICENSE ${TEMP_DIR}/

# Create tarball
cd ${TEMP_DIR}
tar -czf "${PWD}/../${OUTPUT_DIR}/${PACKAGE_NAME}" .
cd -

# Clean up
rm -rf ${TEMP_DIR}

echo "Package created: ${OUTPUT_DIR}/${PACKAGE_NAME}"
echo "SHA256: $(sha256sum ${OUTPUT_DIR}/${PACKAGE_NAME})"

# Verify package integrity
echo "Verifying package..."
tar -tzf ${OUTPUT_DIR}/${PACKAGE_NAME} > /dev/null
echo "Package verification successful!"

echo ""
echo "To install manually:"
echo "  mkdir -p ~/.openclaw/workspace/skills/${SKILL_NAME}"
echo "  tar -xzf ${OUTPUT_DIR}/${PACKAGE_NAME} -C ~/.openclaw/workspace/skills/${SKILL_NAME}"