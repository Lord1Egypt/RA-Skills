# Transfer Service - transfer.whalebone.io

This service provides free file sharing via curl upload similar to transfer.sh.

## How it Works

When you upload a file with:
```bash
curl --upload-file ./localfile.txt https://transfer.whalebone.io/localfile.txt
```

The service returns a URL that can be used to download the file.

## Features

- No registration required
- Files are available for download via the returned URL
- Typically files are stored for a limited time (check service policy)
- Supports any file type
- Uses HTTPS for secure transfer

## Example Response

After uploading, you might see:
```
https://transfer.whalebone.io/abcdef123456/localfile.txt
```

This URL can be shared with others to download the file.

## Notes

- The service may have limits on file size or number of uploads
- Always verify the service's current terms of use
- For sensitive files, consider encrypting before upload