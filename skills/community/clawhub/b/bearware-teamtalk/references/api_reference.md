# TeamTalk 5 SDK API Reference

## Core Client API Functions

### Instance Management
- `TT_InitTeamTalk()` - Create new TeamTalk instance
- `TT_InitTeamTalkEx()` - Create instance with custom settings
- `TT_CloseTeamTalk()` - Close instance
- `TT_DeleteInstance()` - Delete instance (must call after CloseTeamTalk)
- `TT_GetVersion()` - Get SDK version string
- `TT_GetSDKVersion()` - Get SDK version as int

### Connection
- `TT_Connect()` - Connect to server (IP, TCP port, UDP port)
- `TT_ConnectEx()` - Connect with IPv4/IPv6 flags
- `TT_Disconnect()` - Disconnect from server
- `TT_SetEncryptionContext()` - Setup TLS/encryption before connect
- `TT_GetConnectionStatus()` - Get current connection status

### Authentication
- `TT_DoLogin()` - Login with username and password
- `TT_DoLogout()` - Logout
- `TT_DoChangeNickname()` - Change nickname
- `TT_DoChangeStatus()` - Change status message

### Channels
- `TT_DoJoinChannel()` - Join existing channel (or create and join)
- `TT_DoJoinChannelByID()` - Join channel by ID
- `TT_DoLeaveChannel()` - Leave channel
- `TT_DoMakeChannel()` - Create new channel
- `TT_DoUpdateChannel()` - Update channel properties
- `TT_DoRemoveChannel()` - Delete channel
- `TT_DoListChannels()` - List all channels

### Audio
- `TT_InitSoundDevices()` - Initialize sound devices
- `TT_InitSoundDuplexDevices()` - Initialize sound with separate devices
- `TT_OpenSoundInputDevice()` - Open microphone
- `TT_OpenSoundOutputDevice()` - Open speaker/headphones
- `TT_CloseSoundInputDevice()` - Close microphone
- `TT_CloseSoundOutputDevice()` - Close speaker
- `TT_EnableVoiceTransmission()` - Start/stop voice transmission
- `TT_SetSoundInputGain()` - Set microphone gain (0-1000)
- `TT_SetSoundOutputVolume()` - Set speaker volume (0-1000)
- `TT_GetSoundDevices()` - List available sound devices
- `TT_EnableAudioBlockEvent()` - Get raw audio blocks
- `TT_EnableAudioBlockEventEx()` - Get raw audio blocks with stream types
- `TT_SetUserAudioStreamBufferSize()` - Set buffer size for a user
- `TT_SetUserJitterControl()` - Enable jitter buffer
- `TT_GetUserJitterControl()` - Get jitter config
- `TT_SetUserMediaStorageDir()` - Store user audio to disk
- `TT_SetUserMediaStorageDirEx()` - Store audio with close condition

### Video
- `TT_StartVideoCaptureTransmission()` - Start webcam transmission
- `TT_StopVideoCaptureTransmission()` - Stop webcam transmission
- `TT_GetVideoCaptureDevices()` - List webcams
- `TT_SetVideoCaptureDevice()` - Select webcam
- `TT_StartStreamingMediaFileToChannel()` - Stream video file to channel

### Desktop Sharing
- `TT_StartSharingDesktop()` - Start desktop sharing
- `TT_StopSharingDesktop()` - Stop desktop sharing
- `TT_SendDesktopCursorPosition()` - Send mouse cursor position
- `TT_SendDesktopInput()` - Send keyboard/mouse input to shared desktop

### Text Messaging
- `TT_DoTextMessage()` - Send text message (private or channel)
- `TT_DoTextMessageEx()` - Send text message with custom type

### File Sharing
- `TT_DoSendFile()` - Upload file to channel
- `TT_DoRecvFile()` - Download file from channel
- `TT_DoCancelFile()` - Cancel file transfer
- `TT_DoListFiles()` - List files in channel
- `TT_DoRemoveFile()` - Remove file from channel

### User Management
- `TT_DoKickUser()` - Kick user from channel
- `TT_DoBanUser()` - Ban user
- `TT_DoUnBanUser()` - Unban user
- `TT_DoListBans()` - List banned users
- `TT_DoListUsers()` - List users in channel
- `TT_GetUser()` - Get user by ID
- `TT_GetMyUser()` - Get own user object
- `TT_DoChangeUserType()` - Change user type (operator, etc.)
- `TT_DoChangeSubscribe()` - Change user subscription

### User Accounts
- `TT_DoListUserAccounts()` - List all user accounts
- `TT_DoNewUserAccount()` - Create user account
- `TT_DoDeleteUserAccount()` - Delete user account
- `TT_DoUpdateUserAccount()` - Update user account

### Media Files
- `TT_StartStreamingMediaFileToChannel()` - Stream media file
- `TT_StopStreamingMediaFileToChannel()` - Stop streaming
- `TT_InitLocalPlayback()` - Play media file locally
- `TT_CloseLocalPlayback()` - Stop local playback
- `TT_StartRecordingMuxedStreams()` - Record mixed audio to file
- `TT_StartRecordingMuxedAudioFile()` - Record all audio to single file

### Server Administration
- `TT_DoUpdateServer()` - Update server properties
- `TT_GetServerProperties()` - Get server properties
- `TT_GetServerStatistics()` - Get server stats

## Core Server API Functions

- `TTS_InitTeamTalkServer()` - Initialize server instance
- `TTS_InitTeamTalkServerEx()` - Initialize with custom settings
- `TTS_CloseServer()` - Shutdown server
- `TTS_RunServer()` - Run server (blocking)
- `TTS_LoadConfiguration()` - Load config from XML
- `TTS_SaveConfiguration()` - Save config to XML
- `TTS_SetEncryptionContext()` - Set TLS certificate/key
- `TTS_SetEncryptionContextEx()` - Set per-instance encryption

## Key Enumerations

### StreamType
- `STREAMTYPE_VOICE` - Microphone audio
- `STREAMTYPE_VIDEOCAPTURE` - Webcam video
- `STREAMTYPE_DESKTOP` - Desktop sharing
- `STREAMTYPE_MEDIAFILE_AUDIO` - Streamed audio file
- `STREAMTYPE_MEDIAFILE_VIDEO` - Streamed video file
- `STREAMTYPE_MEDIAFILE` - Both audio+video media file
- `STREAMTYPE_CHANNELMSG` - Channel text messages
- `STREAMTYPE_LOCALMEDIAPLAYBACK_AUDIO` - Local playback audio

### ChannelType
- `CHANNEL_DEFAULT` - Normal channel
- `CHANNEL_CLASSROOM` - Teacher-controlled transmission
- `CHANNEL_SOLO_TRANSMIT` - One user at a time
- `CHANNEL_FREEFORALL` - Override classroom
- `CHANNEL_HIDDEN` - Hidden from non-privileged users

### UserType
- `USERTYPE_DEFAULT` - Regular user
- `USERTYPE_ADMIN` - Administrator
- `USERTYPE_NONE` - Not logged in

### UserRight
- `USERRIGHT_DEFAULT` - No special rights
- `USERRIGHT_VIEW_HIDDEN_CHANNELS`
- `USERRIGHT_TEXTMESSAGE_USER`
- `USERRIGHT_TEXTMESSAGE_CHANNEL`
- `USERRIGHT_MODIFY_CHANNELS`
- `USERRIGHT_MULTI_LOGIN`

### SoundSystem
- `SOUNDSYSTEM_WASAPI` - Windows Audio Session API
- `SOUNDSYSTEM_DIRECTSOUND` - DirectSound
- `SOUNDSYSTEM_WINMM` - Windows Multimedia
- `SOUNDSYSTEM_COREAUDIO` - macOS CoreAudio
- `SOUNDSYSTEM_ALSA` - Linux ALSA
- `SOUNDSYSTEM_PULSEAUDIO` - Linux PulseAudio
- `SOUNDSYSTEM_OPENSLES` - Android OpenSL ES

### AudioPreprocessor
- `AUDIOPREPROCESSOR_NONE` - No preprocessor
- `AUDIOPREPROCESSOR_SPEEXDSP` - Speex DSP
- `AUDIOPREPROCESSOR_WEBRTC` - WebRTC audio preprocessor

### AudioFileFormat
- `AFF_WAV_FORMAT` - WAV
- `AFF_MP3_FORMAT` - MP3 (128 kbit)
- `AFF_MP3_320KBIT_FORMAT` - MP3 (320 kbit)
- `AFF_OGG_VORBIS_FORMAT` - OGG Vorbis
- `AFF_OGG_OPUS_FORMAT` - OGG Opus
- `AFF_WMA_FORMAT` - WMA

### ClientError
- `CMDERR_SUCCESS` - Command succeeded
- `CMDERR_FAILED` - Generic failure
- `CMDERR_INSUFFICIENT_USER_RIGHTS` - User lacks permission
- `CMDERR_INVALID_CHANNEL` - Channel doesn't exist
- `CMDERR_CHANNEL_CANNOT_BE_HIDDEN` - Can't hide this channel
- `CMDERR_MAX_FILETRANSFERS_EXCEEDED` - Too many file transfers
- `CMDERR_SOUND_ERROR` - Sound system error

### ClientEvent
- `CLIENTEVENT_CON_SUCCESS` - Connected
- `CLIENTEVENT_CON_LOST` - Connection lost
- `CLIENTEVENT_CON_FAILED` - Connection failed
- `CLIENTEVENT_CON_CRYPT_ERROR` - Encryption error
- `CLIENTEVENT_USER_LOGGEDIN` - User logged in
- `CLIENTEVENT_USER_LOGGEDOUT` - User logged out
- `CLIENTEVENT_USER_JOINED` - User joined channel
- `CLIENTEVENT_USER_LEFT` - User left channel
- `CLIENTEVENT_USER_UPDATE` - User updated
- `CLIENTEVENT_USER_FIRSTVOICESTREAMPACKET` - First voice packet
- `CLIENTEVENT_USER_STATECHANGE` - User state change
- `CLIENTEVENT_CHANNEL_NEW` - Channel created
- `CLIENTEVENT_CHANNEL_UPDATE` - Channel updated
- `CLIENTEVENT_CHANNEL_REMOVE` - Channel removed
- `CLIENTEVENT_CMD_MYSELF_LOGGEDIN` - Self logged in
- `CLIENTEVENT_CMD_MYSELF_LOGGEDOUT` - Self logged out
- `CLIENTEVENT_CMD_USER_ACCOUNT_NEW` - User account created
- `CLIENTEVENT_CMD_USER_ACCOUNT_REMOVE` - User account removed
- `CLIENTEVENT_CMD_ERROR` - Command error
- `CLIENTEVENT_INTERNAL_ERROR` - Internal error
- `CLIENTEVENT_SOUNDDEVICE_ADDED` - Sound device added
- `CLIENTEVENT_SOUNDDEVICE_REMOVED` - Sound device removed
- `CLIENTEVENT_SOUNDDEVICE_UNPLUGGED` - Sound device unplugged
- `CLIENTEVENT_SOUNDDEVICE_NEW_DEFAULT_INPUT` - New default input
- `CLIENTEVENT_SOUNDDEVICE_NEW_DEFAULT_OUTPUT` - New default output
- `CLIENTEVENT_FILETRANSFER` - File transfer event
- `CLIENTEVENT_STREAM_STARTED` - Stream started
- `CLIENTEVENT_STREAM_STOPPED` - Stream stopped
- `CLIENTEVENT_VIDEOCAPTURE_STARTED` - Video capture started
- `CLIENTEVENT_VIDEOCAPTURE_STOPPED` - Video capture stopped
- `CLIENTEVENT_AUDIOBLOCK` - Audio block received
- `CLIENTEVENT_USER_RECORD_MEDIA` - User recording media
- `CLIENTEVENT_TTS_ERROR` - TTS error
- `CLIENTEVENT_CUSTOM_MESSAGE` - Custom message received
- `CLIENTEVENT_CLASSROOM` - Classroom event
- `CLIENTEVENT_DESKTOP_WINDOW_TRANSMIT` - Desktop sharing event

### ServerLogEvent
- `SERVERLOGEVENT_USER_LOGGEDIN`
- `SERVERLOGEVENT_USER_LOGGEDOUT`
- `SERVERLOGEVENT_USER_CRYPTERROR`
- `SERVERLOGEVENT_USER_NEW_STREAM`

## Key Structs

### User
- `nUserID` - Unique user ID
- `szUsername` - Username
- `szNickname` - Display name
- `nUserType` - UserType enum
- `uUserRights` - Bitmask of UserRight
- `szIPAddress` - IP address
- `nChannelID` - Current channel ID
- `uLocalSubscriptions` - Subscription flags
- `nStatusMode` - Status mode
- `szStatusMessage` - Status text
- `szClientName` - Client software name (v5.2a+)
- `bMute` - Muted flag
- `bStreamAudio` - Audio stream active
- `bStreamVideo` - Video stream active
- `bStreamDesktop` - Desktop sharing active
- `bStreamMediaFile` - Media file streaming

### Channel
- `nChannelID` - Unique channel ID
- `nParentID` - Parent channel ID
- `szName` - Channel name
- `szPassword` - Channel password (empty = no password)
- `szTopic` - Channel topic
- `uChannelType` - ChannelType bitmask
- `nDiskQuota` - Disk quota in MB
- `nMaxUsers` - Max users (0 = unlimited)
- `nAudioCodec` - AudioCodec
- `nVideoCodec` - VideoCodec
- `nTimeOutTimerVoiceMSec` - Voice stream timeout (v5.14a+)
- `nTimeOutTimerMediaFileMSec` - Media stream timeout (v5.14a+)
- `nTransmitUsersQueueDelayMSec` - Solo transmit delay (v5.9a+)

### UserAccount
- `szUsername` - Login name
- `szPassword` - Password
- `szNote` - Note/description
- `nUserType` - UserType
- `uUserRights` - Bitmask of UserRight
- `nAudioCodec` - Audio codec bitrate limit
- `nAudioBitRate` - Audio bitrate limit
- `nVideoCodec` - Video codec
- `nVideoBitRate` - Video bitrate limit
- `nMaxLoginAttempts` - Max login attempts
- `szLastLoginTime` - Last login timestamp (v5.18a+)
- `szLastModified` - Last modified timestamp (v5.8b+)

### TextMessage
- `nFromUserID` - Sender user ID
- `nToUserID` - Recipient (0 = channel)
- `nChannelID` - Target channel
- `szMessage` - Message content (max 511 chars)
- `bMore` - Part of combined message (v5.9a+)

### ServerProperties
- `szServerName` - Server name
- `szMOTD` - Message of the day
- `szMOTDURL` - MOTD URL
- `nMaxUsers` - Max concurrent users
- `uServerLogEvents` - ServerLogEvent bitmask (v5.9a+)

### AudioCodec
- `nCodec` - Codec type (OPUS/Speex)
- `nSampleRate` - Sample rate (Hz)
- `nChannels` - Number of channels (1=mono, 2=stereo)
- `nBitRate` - Bitrate (bps)
- `nTxIntervalMSec` - Transmission interval

### VideoCodec
- `nCodec` - Codec type (WebM VP8)
- `nFPS` - Frames per second
- `nWidth` - Frame width
- `nHeight` - Frame height
- `nBitRate` - Bitrate
- `nRaster` - Raster/format
- `nOptions` - Options (VBR/CBR)

### SoundDevice
- `nSoundSystem` - SoundSystem enum
- `szDeviceName` - Device name
- `nDeviceID` - Device ID (deprecated v5.22a)
- `uFeatures` - SoundDeviceFeature bitmask
- `uMaxInputChannels` - Max input channels
- `uMaxOutputChannels` - Max output channels
- `nDefaultSampleRate` - Default sample rate
- `nMaxSampleRate` - Max supported sample rate
- `bDefaultDevice` - Is default device
- `nWaveDeviceID` - Wave device ID (deprecated v5.22a)

### AudioBlock
- `nUserID` - User who produced audio
- `szUserID` - User ID string
- `nStreamType` - Stream type
- `uStreamTypes` - Mixed stream types (v5.8a+)
- `nSampleRate` - Sample rate
- `nChannels` - Number of channels
- `nSamples` - Number of audio samples
- `audioBuffer` - Raw PCM data

### AudioPreprocessor
- `nPreprocessor` - AudioPreprocessor enum
- `speexdsp` - SpeexDSP config (union)
- `webrtc` - WebRTCAudioPreprocessor config (v5.7a+)

### WebRTCAudioPreprocessor
- `extensions` - Extension flags
- `noise_suppression` - Noise suppression level
- `gain_control` - AGC mode
- `echo_suppression` - Echo suppression
- `echo_type` - Echo type
- `highpass_filter` - HPF enabled
- `experimental_agc` - Experimental AGC
- (v5.18a: removed voicedetection, levelestimation, modified adaptivedigital)

### EncryptionContext
- `bVerifyPeer` - Verify remote peer
- `szCAFile` - CA certificate file
- `szCAPath` - CA certificate path
- `szCertificateFile` - Local certificate
- `szPrivateKeyFile` - Private key file
- `szCipherList` - Allowed ciphers

### JitterConfig
- `bEnableJitterControl` - Enable jitter buffer
- `nMaxDelay` - Maximum delay in ms

### ClientStatistics
- `nUDPBytesIn` - UDP bytes received
- `nUDPBytesOut` - UDP bytes sent
- `nTCPBytesIn` - TCP bytes received
- `nTCPBytesOut` - TCP bytes sent
- `nUDPPacketsIn` - UDP packets received
- `nUDPPacketsOut` - UDP packets sent
- `nVoicePacketsRecv` - Voice packets received
- `nVoicePacketsLost` - Voice packets lost
- `nSoundInputDeviceDelayMSec` - Audio device delay (v5.7a+)
