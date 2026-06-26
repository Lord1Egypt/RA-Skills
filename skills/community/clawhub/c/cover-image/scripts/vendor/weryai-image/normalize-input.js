export function normalizeImageInput(rawInput) {
  const input = { ...rawInput };
  const singleImage =
    input.image ??
    input.source_image ??
    input.sourceImage ??
    input.reference_image ??
    input.referenceImage;

  if ((!Array.isArray(input.images) || input.images.length === 0) && typeof singleImage === 'string' && singleImage) {
    input.images = [singleImage];
  }

  return input;
}

export function detectImageMode(input) {
  if (Array.isArray(input.images) && input.images.length > 0) return 'image_to_image';
  return 'text_to_image';
}
