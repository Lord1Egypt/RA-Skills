# TeamTalk 5 SDK ChangeLog

## v5.22a (April 8, 2026)
- Windows can now stream AAC, Vorbis, and other formats (previously Linux/Mac only)
- New `SERVERLOGEVENT_USER_CRYPTERROR` - encryption error log event
- New `SERVERLOGEVENT_USER_NEW_STREAM` - new stream log event
- Deprecated `nWaveDeviceID` in `SoundDevice`

## v5.19a (August 5, 2025)
- Security fix: reused channel ID could give operator access

## v5.18a (May 5, 2025)
- `UserAccount.szLastLoginTime` - last login timestamp
- WebRTC updated to r6818 (breaking change: removed voicedetection, levelestimation)

## v5.15a (December 19, 2023)
- PulseAudio support for Ubuntu 22 and Raspbian
- `USERRIGHT_TEXTMESSAGE_USER` and `USERRIGHT_TEXTMESSAGE_CHANNEL`
- `CMDERR_MAX_FILETRANSFERS_EXCEEDED`

## v5.14a (August 16, 2023)
- Time-out timer for voice/media streams (`nTimeOutTimerVoiceMSec`, `nTimeOutTimerMediaFileMSec`)

## v5.13a (May 8, 2023)
- `CLIENTEVENT_CON_CRYPT_ERROR` for encrypted connection failures
- Events for user account added/removed
- Non-blocking encrypted connect
- Sound device change events (Windows)

## v5.12a (December 21, 2022)
- Crash fix: channel ban on user not in channel

## v5.11a (October 2, 2022)
- Server restores classroom transmissions after reconnect
- Standard server no longer depends on OpenSSL
- Pro server requires WebLogin auth
- Subscription changes logged
- Ubuntu 22 target (replaces Ubuntu 18)
- `MSGTYPE_NONE`

## v5.9a (April 2, 2022)
- Configurable server logging (`ServerLogEvents`)
- Combined text messages (`bMore` flag)
- Configurable solo transmit delay (`nTransmitUsersQueueDelayMSec`)

## v5.8b (September 7, 2021)
- `szLastModified` on UserAccount
- `szUploadTime` on RemoteFile

## v5.8a (June 24, 2021)
- Mix multiple stream types into single audio file
- `TT_StartRecordingMuxedStreams()`
- `STREAMTYPE_LOCALMEDIAPLAYBACK_AUDIO`

## v5.7a (March 4, 2021)
- WebRTC Audio Preprocessor (replaces SpeexDSP)
- Classroom support for channel text messages
- Hidden channels (`CHANNEL_HIDDEN`)
- Client/Server TLS peer verification
- Jitter buffer (`JitterConfig`)
- OPUS .ogg streaming on Windows
- Multiple encryption contexts per server

## v5.6a (August 9, 2020)
- Android voice communication mode
- Platform-specific sound device effects
- Configurable shared sound device sample rate/channels
- Sound loopback test
- Sound preprocessor selection

## v5.5a (April 13, 2020)
- Shared audio input/output device
- Media file playback control
- OPUS codec frame size selection
- Muxed audio stream access
- Inject audio into channel
- TCP/UDP keep alive configuration
- Multi-channel audio recording
- Encrypted server connection support
- Android C-API shared library

## v5.4a (June 25, 2019)
- Various features and bug fixes

## v5.3b (November 11, 2018)
- API changes

## v5.3a (April 14, 2018)
- API changes

## v5.2d (June 24, 2017)
- Bugfixes

## v5.2c (May 8, 2017)
- Virtual sound device
- Transmission queue in CHANNEL_SOLO_TRANSMIT
- Server callbacks for nickname/status changes
- Daemon scripts for server

## v5.2b (January 30, 2017)
- Send text message from Server API

## v5.2a (January 8, 2017)
- TeamTalk Server API with System ID
- Voice-Processing I/O Unit for iOS
- V4L2 support on Linux
- AVFoundation replaces QTkit on macOS
- Android Studio support
- OGG audio storage
- WebM encoder deadline option
- Client name detection
- Single-client server access limit

## v5.1c (February 29, 2016)
- Bugfixes and API changes

## v5.1b (October 3, 2015)
- Record own voice stream to separate file
- TeamTalk JNI DLL for Windows

## v5.1a (June 13, 2015)
- TeamTalk 5 Server API
- TeamTalk 5 Java DLL
- TeamTalk 5 SDK for iOS

## v5.0a (March 15, 2015)
- Major rewrite from v4
- WebM replaces Theora video codec
- OPUS replaces CELT audio codec
- AES encryption replaces Blowfish
- Media file stream type
- User rights moved to user account
- Audio codec bitrate limit on user account
- Max channels: 4000
- P2P support removed
- Channels can be renamed
- Daemon scripts for server
- Default config: tt5srv.xml
- Server stats updated
- Non-encrypted mode in Pro server
