function line(value: unknown, fallback = "N/A"): string {
  if (value === undefined || value === null || value === "") return fallback;
  return String(value);
}

function bytes(value: unknown): string {
  if (typeof value !== "number" || !Number.isFinite(value)) return "N/A";
  if (value < 1024 * 1024) return `${Math.round(value / 1024)} KB`;
  return `${(value / 1024 / 1024).toFixed(1)} MB`;
}

function duration(value: unknown): string {
  if (typeof value !== "number" || !Number.isFinite(value)) return "N/A";
  return `${value}s`;
}

function stats(item: Record<string, any>): string {
  return `Views: ${line(item.views, "0")} | Downloads: ${line(item.downloads, "0")} | Likes: ${line(item.likes, "0")}`;
}

function pickPexelsVideoFile(files: any[] = []): any | undefined {
  const scored = files.filter(Boolean).map((file) => ({
    file,
    score: (file.quality === "hd" ? 1_000_000_000 : 0) + (Number(file.width) || 0) * (Number(file.height) || 0),
  }));
  scored.sort((a, b) => b.score - a.score);
  return scored[0]?.file;
}

function pickPixabayVideo(videos: Record<string, any> = {}): any | undefined {
  const entries = Object.values(videos).filter(Boolean);
  entries.sort((a, b) => ((Number(b.width) || 0) * (Number(b.height) || 0)) - ((Number(a.width) || 0) * (Number(a.height) || 0)));
  return entries[0];
}

function header(label: string, total: unknown, shown: number): string {
  return `Found ${line(total, String(shown))} ${label} (showing ${shown})`;
}

export function formatPexelsVideos(data: any): string {
  const videos = data.videos ?? [];
  const sections = [header("videos", data.total_results, videos.length)];
  videos.forEach((video: any, index: number) => {
    const file = pickPexelsVideoFile(video.video_files);
    sections.push([
      `\n[${index + 1}] Pexels Video ID: ${line(video.id)}`,
      `Size: ${line(video.width)}x${line(video.height)} | Duration: ${duration(video.duration)}`,
      `Creator: ${line(video.user?.name)}`,
      `Page: ${line(video.url)}`,
      `Thumbnail: ${line(video.image)}`,
      `Download: ${line(file?.link)}`,
      `File: ${line(file?.quality)} ${line(file?.width)}x${line(file?.height)} ${line(file?.file_type)} ${line(file?.fps)}fps ${bytes(file?.size)}`,
    ].join("\n"));
  });
  return sections.join("\n");
}

export function formatPexelsPhotos(data: any): string {
  const photos = data.photos ?? [];
  const sections = [header("photos", data.total_results, photos.length)];
  photos.forEach((photo: any, index: number) => {
    sections.push([
      `\n[${index + 1}] Pexels Photo ID: ${line(photo.id)}`,
      `Alt: ${line(photo.alt)}`,
      `Size: ${line(photo.width)}x${line(photo.height)}`,
      `Photographer: ${line(photo.photographer)}`,
      `Page: ${line(photo.url)}`,
      `Download: ${line(photo.src?.original)}`,
      `Preview: ${line(photo.src?.large ?? photo.src?.medium)}`,
    ].join("\n"));
  });
  return sections.join("\n");
}

export function formatPixabayVideos(data: any): string {
  const hits = data.hits ?? [];
  const sections = [header("videos", data.totalHits, hits.length)];
  hits.forEach((video: any, index: number) => {
    const file = pickPixabayVideo(video.videos);
    sections.push([
      `\n[${index + 1}] Pixabay Video ID: ${line(video.id)}`,
      `Name: ${line(video.name)}`,
      `Tags: ${line(video.tags)}`,
      `Duration: ${duration(video.duration)}`,
      `Creator: ${line(video.user)}`,
      `Page: ${line(video.pageURL)}`,
      `Download: ${line(file?.url)}`,
      `File: ${line(file?.width)}x${line(file?.height)} ${bytes(file?.size)}`,
      `Stats: ${stats(video)}`,
    ].join("\n"));
  });
  return sections.join("\n");
}

export function formatPixabayImages(data: any): string {
  const hits = data.hits ?? [];
  const sections = [header("images", data.totalHits, hits.length)];
  hits.forEach((image: any, index: number) => {
    sections.push([
      `\n[${index + 1}] Pixabay Image ID: ${line(image.id)}`,
      `Name: ${line(image.name)}`,
      `Tags: ${line(image.tags)}`,
      `Type: ${line(image.type)} | Size: ${line(image.imageWidth)}x${line(image.imageHeight)}`,
      `Creator: ${line(image.user)}`,
      `Page: ${line(image.pageURL)}`,
      `Download: ${line(image.largeImageURL)}`,
      `Preview: ${line(image.webformatURL)}`,
      `Stats: ${stats(image)}`,
    ].join("\n"));
  });
  return sections.join("\n");
}

export function formatJamendoTracks(data: any): string {
  const tracks = data.results ?? [];
  const total = data.results_fullcount ?? data.headers?.results_fullcount ?? tracks.length;
  const sections = [header("tracks", total, tracks.length)];
  tracks.forEach((track: any, index: number) => {
    sections.push([
      `\n[${index + 1}] Jamendo Track ID: ${line(track.id)}`,
      `Name: ${line(track.name)}`,
      `Artist: ${line(track.artist_name)}`,
      `Album: ${line(track.album_name)}`,
      `Duration: ${duration(track.duration)}`,
      `License: ${line(track.license_ccurl)}`,
      `Stream: ${line(track.audio)}`,
      `Download: ${track.audiodownload ? track.audiodownload : "Download not available"}`,
      `Download Allowed: ${line(track.audiodownload_allowed)}`,
      `Page: ${line(track.shareurl)}`,
      `Pro: ${line(track.prourl)}`,
    ].join("\n"));
  });
  return sections.join("\n");
}

export function formatJamendoAlbums(data: any): string {
  const albums = data.results ?? [];
  const sections = [header("albums", data.results_fullcount ?? data.headers?.results_fullcount, albums.length)];
  albums.forEach((album: any, index: number) => {
    sections.push([
      `\n[${index + 1}] Jamendo Album ID: ${line(album.id)}`,
      `Name: ${line(album.name)}`,
      `Artist: ${line(album.artist_name)}`,
      `Released: ${line(album.releasedate)}`,
      `Tracks: ${line(album.zip)}`,
      `Page: ${line(album.shareurl)}`,
      `Image: ${line(album.image)}`,
    ].join("\n"));
  });
  return sections.join("\n");
}

export function formatJamendoArtists(data: any): string {
  const artists = data.results ?? [];
  const sections = [header("artists", data.results_fullcount ?? data.headers?.results_fullcount, artists.length)];
  artists.forEach((artist: any, index: number) => {
    sections.push([
      `\n[${index + 1}] Jamendo Artist ID: ${line(artist.id)}`,
      `Name: ${line(artist.name)}`,
      `Website: ${line(artist.website)}`,
      `Page: ${line(artist.shareurl)}`,
      `Image: ${line(artist.image)}`,
    ].join("\n"));
  });
  return sections.join("\n");
}

export function formatFreesoundResults(data: any): string {
  const sounds = data.results ?? [];
  const sections = [header("sounds", data.count, sounds.length)];
  sounds.forEach((sound: any, index: number) => {
    const preview = sound.previews?.["preview-hq-mp3"] ?? sound.previews?.["preview-lq-mp3"];
    sections.push([
      `\n[${index + 1}] Freesound ID: ${line(sound.id)}`,
      `Name: ${line(sound.name)}`,
      `Creator: ${line(sound.username)}`,
      `Duration: ${duration(sound.duration)}`,
      `License: ${line(sound.license)}`,
      `Tags: ${Array.isArray(sound.tags) ? sound.tags.join(", ") : line(sound.tags)}`,
      `Page: ${line(sound.url)}`,
      `Preview: ${line(preview)}`,
      `Download: bun ./scripts/freesound.ts download --id ${line(sound.id)} --output ./sound-${line(sound.id)}.mp3`,
    ].join("\n"));
  });
  return sections.join("\n");
}

export function formatFreesoundComments(data: any): string {
  const comments = data.results ?? [];
  const sections = [header("comments", data.count, comments.length)];
  comments.forEach((comment: any, index: number) => {
    sections.push([
      `\n[${index + 1}] Comment ID: ${line(comment.id)}`,
      `User: ${line(comment.username)}`,
      `Created: ${line(comment.created)}`,
      `Comment: ${line(comment.comment)}`,
    ].join("\n"));
  });
  return sections.join("\n");
}
