# Windows Disk Cleaner

## Folders to Clean

### Temp Files
- `%TEMP%` (user temp folder)
- `%TMP%` (alternate temp folder)
- `C:\Windows\Temp`

### Browser Cache
- Chrome: `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache`
- Edge: `%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache`
- Firefox: `%LOCALAPPDATA%\Mozilla\Firefox\Profiles`

### Recycle Bin
- Empty the Windows Recycle Bin completely

### Log Files
- `C:\Windows\Logs`
- `C:\Windows\SoftwareDistribution\Download`

## Safety Rules
- Never delete anything in `C:\Windows\System32`
- Never delete anything in `C:\Program Files`
- Never delete user Documents, Downloads, Desktop, Pictures, Videos
- Only delete files older than 1 day
- If unsure about a file — skip it

## Steps
1. Check if folder exists before cleaning
2. Calculate folder size before deleting
3. If Confirm Mode — ask user before each folder
4. Delete all files inside the folder (not the folder itself)
5. Show how much space was freed after each step
6. Show total space freed at the end
