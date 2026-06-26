export const MOCK_DESCRIBE_PROJECT = [
  {
    // "ProjectName": 'Mock AIDP项目',
    LatestEditParam: {
      Canvas: {
        Width: 1920,
        Height: 1080,
        BackgroundColor: '#000000FF',
      },
      Track: [],
    },
  },
]

// searchEditMaterial 期望返回 { Total, Detail }
// Detail 每项: Name, EditMid, Source (vid://xxx | mid://xxx), Type (video|audio|image)
// 之后编辑器会对每条再调 getVideoInfo(video/audio) 或 mGetMaterial(image) 补详情
export const MOCK_SEARCH_EDIT_MATERIAL = {
  Total: 9,
  Detail: [
    {
      EditMid: 'm02bd00d3tlh09vtk12qe2o8b30',
      ProjectId: 'p024600d3nl788u77eiocql5k50',
      Name: '下载.mp3',
      Type: 'audio',
      Status: 'Failed',
      Source: 'vid://v02bffg10064d30igdqljht5q0mvetjg',
      Content: {},
      CreatedAt: '2025-10-24T18:44:18+08:00',
      UpdatedAt: '2025-10-24T18:44:18+08:00',
      Extra: '',
    },
    {
      EditMid: 'm02af00d40cthgk5gt3ts3hbba0',
      ProjectId: 'p024600d3nl788u77eiocql5k50',
      Name: '',
      Type: 'video',
      Status: 'Completed',
      Source: 'vid://v0dbffg10064d406uhqljht6tre6u5b0',
      Content: {
        Sprite: {
          Format: 'jpeg',
          StoreUrls: [
            'https://console-image-cn.volcvod.com/aideo-dev/c0a5c4f215d5456bbde831a3d3ec7bb6~noop.image?sign=1769676640-r0-u0-a002495a0bc733a594a8ee5a00dc61d0',
          ],
          ImgXLen: 5,
          ImgYLen: 5,
          CellWidth: 136,
          CellHeight: 240,
          Interval: 1,
          CaptureNum: 10,
        },
      },
      CreatedAt: '2025-10-28T22:10:14+08:00',
      UpdatedAt: '2025-10-28T22:10:20+08:00',
      Extra: '',
    },
    {
      EditMid: 'm029500d41j94iqsb7ai48hi3f0',
      ProjectId: 'p024600d3nl788u77eiocql5k50',
      Name: 'split_55.mp4',
      Type: 'video',
      Status: 'Completed',
      Source: 'vid://v02bffg10064d3vjq9aljht6ujf4ij5g',
      Content: {
        Sprite: {
          Format: 'jpeg',
          StoreUrls: [
            'https://console-image-cn.volcvod.com/aideo-dev/07488a6a761f4cdd9c4face89cad7dc6~noop.image?sign=1770023668-r0-u0-4f193db285d042335f2116329d225c4f',
          ],
          ImgXLen: 5,
          ImgYLen: 5,
          CellWidth: 136,
          CellHeight: 240,
          Interval: 1,
          CaptureNum: 2,
        },
      },
      CreatedAt: '2025-10-30T17:49:06+08:00',
      UpdatedAt: '2025-10-30T17:49:06+08:00',
      Extra: '',
    },
    {
      EditMid: 'm026b00d41j94hg3f82h8c9a3a0',
      ProjectId: 'p024600d3nl788u77eiocql5k50',
      Name: 'split_54.mp4',
      Type: 'video',
      Status: 'Completed',
      Source: 'vid://v02bffg10064d3vjq9aljht0oe413p20',
      Content: {
        Sprite: {
          Format: 'jpeg',
          StoreUrls: [
            'https://console-image-cn.volcvod.com/aideo-dev/07488a6a761f4cdd9c4face89cad7dc6~noop.image?sign=1769676640-r0-u0-1060bb4d9da950c3c417ff1f95e3ffc0',
          ],
          ImgXLen: 5,
          ImgYLen: 5,
          CellWidth: 136,
          CellHeight: 240,
          Interval: 1,
          CaptureNum: 3,
        },
      },
      CreatedAt: '2025-10-30T17:49:06+08:00',
      UpdatedAt: '2025-10-30T17:49:06+08:00',
      Extra: '',
    },
    {
      EditMid: 'm025100d41j94he7q01h1h0utj0',
      ProjectId: 'p024600d3nl788u77eiocql5k50',
      Name: 'split_34.mp4',
      Type: 'video',
      Status: 'Completed',
      Source: 'vid://v02bffg10064d3vjq82ljhtejm9u1uog',
      Content: {
        Sprite: {
          Format: 'jpeg',
          StoreUrls: [
            'https://console-image-cn.volcvod.com/aideo-dev/7c3d3a6c4f534648b56aa691d14fd10c~noop.image?sign=1769676640-r0-u0-118ee6b0012b65a7a9fcfa21ebd7b478',
          ],
          ImgXLen: 5,
          ImgYLen: 5,
          CellWidth: 136,
          CellHeight: 240,
          Interval: 1,
          CaptureNum: 4,
        },
      },
      CreatedAt: '2025-10-30T17:49:06+08:00',
      UpdatedAt: '2025-10-30T17:49:06+08:00',
      Extra: '',
    },
    {
      EditMid: 'm02af00d41j94gk5gt3ts3hbbbg',
      ProjectId: 'p024600d3nl788u77eiocql5k50',
      Name: 'split_48.mp4',
      Type: 'video',
      Status: 'Completed',
      Source: 'vid://v02bffg10064d3vjq8qljht4tvopr0bg',
      Content: {
        Sprite: {
          Format: 'jpeg',
          StoreUrls: [
            'https://console-image-cn.volcvod.com/aideo-dev/869fc58d581c43f0833ff510cf065994~noop.image?sign=1769676640-r0-u0-789f395b3ffb0efaf777bf0d17bdb79c',
          ],
          ImgXLen: 5,
          ImgYLen: 5,
          CellWidth: 136,
          CellHeight: 240,
          Interval: 1,
          CaptureNum: 1,
        },
      },
      CreatedAt: '2025-10-30T17:49:06+08:00',
      UpdatedAt: '2025-10-30T17:49:06+08:00',
      Extra: '',
    },
    {
      EditMid: 'm025100d41j94he7q01h1h0utjg',
      ProjectId: 'p024600d3nl788u77eiocql5k50',
      Name: 'split_50.mp4',
      Type: 'video',
      Status: 'Completed',
      Source: 'vid://v02bffg10064d3vjq92ljhtbribb9sq0',
      Content: {
        Sprite: {
          Format: 'jpeg',
          StoreUrls: [
            'https://console-image-cn.volcvod.com/aideo-dev/5b8632e10a8e4ac1a11f592f57e39380~noop.image?sign=1769676640-r0-u0-5c51ecbb95e5d30174b74f8294139c20',
          ],
          ImgXLen: 5,
          ImgYLen: 5,
          CellWidth: 136,
          CellHeight: 240,
          Interval: 1,
          CaptureNum: 2,
        },
      },
      CreatedAt: '2025-10-30T17:49:06+08:00',
      UpdatedAt: '2025-10-30T17:49:06+08:00',
      Extra: '',
    },
    {
      EditMid: 'm02e200d41j94ime1pcg60li660',
      ProjectId: 'p024600d3nl788u77eiocql5k50',
      Name: 'split_51.mp4',
      Type: 'video',
      Status: 'Completed',
      Source: 'vid://v02bffg10064d3vjq92ljhtbffh24lsg',
      Content: {
        Sprite: {
          Format: 'jpeg',
          StoreUrls: [
            'https://console-image-cn.volcvod.com/aideo-dev/e7c11288c56e49e5b917a5e6ea46a369~noop.image?sign=1769676640-r0-u0-55b5bf27c805ff82ef9f83b57fdb4400',
          ],
          ImgXLen: 5,
          ImgYLen: 5,
          CellWidth: 136,
          CellHeight: 240,
          Interval: 1,
          CaptureNum: 2,
        },
      },
      CreatedAt: '2025-10-30T17:49:06+08:00',
      UpdatedAt: '2025-10-30T17:49:06+08:00',
      Extra: '',
    },
    {
      EditMid: 'm028e00d41j94j4m8fsvh10ccig',
      ProjectId: 'p024600d3nl788u77eiocql5k50',
      Name: 'split_46.mp4',
      Type: 'video',
      Status: 'Completed',
      Source: 'vid://v02bffg10064d3vjq8qljhta4p6vrss0',
      Content: {
        Sprite: {
          Format: 'jpeg',
          StoreUrls: [
            'https://console-image-cn.volcvod.com/aideo-dev/30f8eb1ecb7947acb61bc00f7c2b6682~noop.image?sign=1769676640-r0-u0-68640c2fc375adf07c90070bb6e6ee1b',
          ],
          ImgXLen: 5,
          ImgYLen: 5,
          CellWidth: 136,
          CellHeight: 240,
          Interval: 1,
          CaptureNum: 5,
        },
      },
      CreatedAt: '2025-10-30T17:49:06+08:00',
      UpdatedAt: '2025-10-30T17:49:06+08:00',
      Extra: '',
    },
  ],
}

// getVideoInfo 按 Vid 匹配的 mock 返回值（Vid = 素材 Source 去掉 "vid://" 后的值）
export const MOCK_GET_VIDEO_INFO_BY_VID = {
  v02bffg10064d30igdqljht5q0mvetjg: {
    Title: '下载.mp3',
    Vid: 'v02bffg10064d30igdqljht5q0mvetjg',
    Filename: '下载.mp3',
    PublishStatus: 'Published',
    Duration: 21.644,
    Codec: 'mp3',
    Height: 0,
    Width: 0,
    Format: 'MP3',
    Size: 347368,
    Bitrate: 128394,
    Tags: [],
    Description: '',
    PosterUrl:
      'https://console-image-cn.volcvod.com/~noop.jpeg?sign=1769680056-r0-u0-48697b269df27915f3922c0d2ca783c7',
    PlayInfo: {
      MainPlayUrl:
        'https://vod-fe-test-aideo.byte-test.com/%E4%B8%8B%E8%BD%BD.mp3?auth_key=1772272056-9e077c0cdde1498f855940887098a64b-0-c9d6b59a69db7400ff59e4f368b98f08',
      BackupPlayUrl:
        'https://vod-fe-test-aideo.byte-test.com/%E4%B8%8B%E8%BD%BD.mp3?auth_key=1772272056-b2ef3efb3b2449b982eaa86dc680c43a-0-9da133b3a315733d9d6dabb0d7bf3a3b',
      Status: 1,
    },
    PosterInfo: {
      MainPosterUri: '',
      BackupPosterUris: [],
      MainPosterInfo: {
        PosterUri: '',
        PosterUrl:
          'https://console-image-cn.volcvod.com/~noop.jpeg?sign=1769680056-r0-u0-48697b269df27915f3922c0d2ca783c7',
      },
      BackupPosterInfo: [],
    },
    CreatedTime: '2025-9-10 15:26:48',
    UpdatedTime: '2025-9-10 15:26:49',
    CategoryTags: [],
    Classification: null,
    TosStorageClass: 'STANDARD',
    DynamicRange: 'SDR',
    OuterPosterUrl: '',
    FileType: 'audio',
    StoreUri: 'aideo-dev/下载.mp3',
    Md5: 'c373c73379c20d28800ea60db32df6da',
    VodUploadSource: 'upload',
    BlockStatus: '',
    HlsMediaSize: 0,
    MainPlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/%E4%B8%8B%E8%BD%BD.mp3?auth_key=1772272056-9e077c0cdde1498f855940887098a64b-0-c9d6b59a69db7400ff59e4f368b98f08',
    BackupPlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/%E4%B8%8B%E8%BD%BD.mp3?auth_key=1772272056-b2ef3efb3b2449b982eaa86dc680c43a-0-9da133b3a315733d9d6dabb0d7bf3a3b',
    Status: 1,
    PlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/%E4%B8%8B%E8%BD%BD.mp3?auth_key=1772272056-9e077c0cdde1498f855940887098a64b-0-c9d6b59a69db7400ff59e4f368b98f08',
  },
  // 可在此继续按 Vid 追加更多条目
  v02bffg10064d3vjq8qljhta4p6vrss0: {
    Title: 'split_46.mp4',
    Vid: 'v02bffg10064d3vjq8qljhta4p6vrss0',
    Filename: 'split_46.mp4',
    PublishStatus: 'Published',
    Duration: 5,
    Codec: 'h264',
    Height: 1920,
    Width: 1080,
    Format: 'MP4',
    Size: 1862730,
    Bitrate: 2980368,
    Tags: [],
    Description: '',
    PosterUrl:
      'https://console-image-cn.volcvod.com/aideo-dev/oUOfenDMjgvlg8RpX31DQe2GzIqpjUEQzRymff~noop.jpeg?sign=1769680345-r0-u0-7ea4f1881aec3d987ebbe583d8c8ed71',
    PlayInfo: {
      MainPlayUrl:
        'https://vod-fe-test-aideo.byte-test.com/split_46.mp4?auth_key=1772272345-e3667e6549b3423bacf4e85d3d8b7c29-0-3f84896fa481feeac0f8a98c164e9a76',
      BackupPlayUrl:
        'https://vod-fe-test-aideo.byte-test.com/split_46.mp4?auth_key=1772272345-43c8a7fbe8fd49c199d3d06ed8d8430a-0-a674c426e509a2c34bf7488f8387c076',
      Status: 1,
    },
    PosterInfo: {
      MainPosterUri: 'aideo-dev/oUOfenDMjgvlg8RpX31DQe2GzIqpjUEQzRymff',
      BackupPosterUris: [],
      MainPosterInfo: {
        PosterUri: 'aideo-dev/oUOfenDMjgvlg8RpX31DQe2GzIqpjUEQzRymff',
        PosterUrl:
          'https://console-image-cn.volcvod.com/aideo-dev/oUOfenDMjgvlg8RpX31DQe2GzIqpjUEQzRymff~noop.jpeg?sign=1769680345-r0-u0-7ea4f1881aec3d987ebbe583d8c8ed71',
      },
      BackupPosterInfo: [],
    },
    CreatedTime: '2025-10-27 17:36:39',
    UpdatedTime: '2025-10-27 17:36:40',
    CategoryTags: [],
    Classification: null,
    TosStorageClass: 'STANDARD',
    DynamicRange: 'SDR',
    OuterPosterUrl:
      'https://vod-fe-test-aideo-img.byte-test.com/aideo-dev/oUOfenDMjgvlg8RpX31DQe2GzIqpjUEQzRymff~tplv-vod-noop.image',
    FileType: 'video',
    StoreUri: 'aideo-dev/split_46.mp4',
    Md5: 'ec0e5ad5fd380318cc04b0c1d464b18e',
    VodUploadSource: 'upload',
    BlockStatus: '',
    HlsMediaSize: 0,
    MainPlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/split_46.mp4?auth_key=1772272345-e3667e6549b3423bacf4e85d3d8b7c29-0-3f84896fa481feeac0f8a98c164e9a76',
    BackupPlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/split_46.mp4?auth_key=1772272345-43c8a7fbe8fd49c199d3d06ed8d8430a-0-a674c426e509a2c34bf7488f8387c076',
    Status: 1,
    PlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/split_46.mp4?auth_key=1772272345-e3667e6549b3423bacf4e85d3d8b7c29-0-3f84896fa481feeac0f8a98c164e9a76',
  },
  v0dbffg10064d406uhqljht6tre6u5b0: {
    Title: '',
    Vid: 'v0dbffg10064d406uhqljht6tre6u5b0',
    Filename: 'cd65aeb811b146ffb7b0d3b8b2890776.mp4',
    PublishStatus: 'Published',
    Duration: 10,
    Codec: 'h264',
    Height: 1280,
    Width: 720,
    Format: 'MP4',
    Size: 78363,
    Bitrate: 62690,
    Tags: [],
    Description: '',
    PosterUrl:
      'https://console-image-cn.volcvod.com/aideo-dev/o80A9peuAg3Zfb18BlQPKb9VHGmMb6IxAeaCsG~noop.jpeg?sign=1769680345-r0-u0-4521e640a3a508ba10fbf5ec59c8d130',
    PlayInfo: {
      MainPlayUrl:
        'https://vod-fe-test-aideo.byte-test.com/cd65aeb811b146ffb7b0d3b8b2890776.mp4?auth_key=1772272345-143d19b5150c46ada0f898c37597a8c2-0-e4a704f39af30254f62561bb00829967',
      BackupPlayUrl:
        'https://vod-fe-test-aideo.byte-test.com/cd65aeb811b146ffb7b0d3b8b2890776.mp4?auth_key=1772272345-b5fcb962fcb046489d7757c34b5d1c69-0-ce803923aaa60886603008dce12acfc5',
      Status: 1,
    },
    PosterInfo: {
      MainPosterUri: 'aideo-dev/o80A9peuAg3Zfb18BlQPKb9VHGmMb6IxAeaCsG',
      BackupPosterUris: [],
      MainPosterInfo: {
        PosterUri: 'aideo-dev/o80A9peuAg3Zfb18BlQPKb9VHGmMb6IxAeaCsG',
        PosterUrl:
          'https://console-image-cn.volcvod.com/aideo-dev/o80A9peuAg3Zfb18BlQPKb9VHGmMb6IxAeaCsG~noop.jpeg?sign=1769680345-r0-u0-4521e640a3a508ba10fbf5ec59c8d130',
      },
      BackupPosterInfo: [],
    },
    CreatedTime: '2025-10-28 15:22:48',
    UpdatedTime: '2025-10-28 15:22:50',
    CategoryTags: [],
    Classification: null,
    TosStorageClass: 'STANDARD',
    DynamicRange: 'SDR',
    OuterPosterUrl:
      'https://vod-fe-test-aideo-img.byte-test.com/aideo-dev/o80A9peuAg3Zfb18BlQPKb9VHGmMb6IxAeaCsG~tplv-vod-noop.image',
    FileType: 'video',
    StoreUri: 'aideo-dev/cd65aeb811b146ffb7b0d3b8b2890776.mp4',
    Md5: '350318965a713f046d4ee3ffaf9ddc2f',
    VodUploadSource: 'media_edit',
    BlockStatus: '',
    HlsMediaSize: 0,
    MainPlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/cd65aeb811b146ffb7b0d3b8b2890776.mp4?auth_key=1772272345-143d19b5150c46ada0f898c37597a8c2-0-e4a704f39af30254f62561bb00829967',
    BackupPlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/cd65aeb811b146ffb7b0d3b8b2890776.mp4?auth_key=1772272345-b5fcb962fcb046489d7757c34b5d1c69-0-ce803923aaa60886603008dce12acfc5',
    Status: 1,
    PlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/cd65aeb811b146ffb7b0d3b8b2890776.mp4?auth_key=1772272345-143d19b5150c46ada0f898c37597a8c2-0-e4a704f39af30254f62561bb00829967',
  },
  v02bffg10064d3vjq92ljhtbffh24lsg: {
    Title: 'split_55.mp4',
    Vid: 'v02bffg10064d3vjq9aljht6ujf4ij5g',
    Filename: 'split_55.mp4',
    PublishStatus: 'Published',
    Duration: 2.28,
    Codec: 'h264',
    Height: 1920,
    Width: 1080,
    Format: 'MP4',
    Size: 1146706,
    Bitrate: 4023529,
    Tags: [],
    Description: '',
    PosterUrl:
      'https://console-image-cn.volcvod.com/aideo-dev/o8Ir2ejPffnqppYJfpGvQhKzGY30hfjKEAyXSZ~noop.jpeg?sign=1769680346-r0-u0-c15b908198163f97c1976a4a4a1d9f57',
    PlayInfo: {
      MainPlayUrl:
        'https://vod-fe-test-aideo.byte-test.com/split_55.mp4?auth_key=1772272346-90cac36df3a74bd691c242f175e4368f-0-2bcfc5c3c4e30fe83267ef2b7838b7e4',
      BackupPlayUrl:
        'https://vod-fe-test-aideo.byte-test.com/split_55.mp4?auth_key=1772272346-d46b522ab9af455cb4784120b4539e63-0-b14aa531eeed7b82d51b5de48eae6be6',
      Status: 1,
    },
    PosterInfo: {
      MainPosterUri: 'aideo-dev/o8Ir2ejPffnqppYJfpGvQhKzGY30hfjKEAyXSZ',
      BackupPosterUris: [],
      MainPosterInfo: {
        PosterUri: 'aideo-dev/o8Ir2ejPffnqppYJfpGvQhKzGY30hfjKEAyXSZ',
        PosterUrl:
          'https://console-image-cn.volcvod.com/aideo-dev/o8Ir2ejPffnqppYJfpGvQhKzGY30hfjKEAyXSZ~noop.jpeg?sign=1769680346-r0-u0-c15b908198163f97c1976a4a4a1d9f57',
      },
      BackupPosterInfo: [],
    },
    CreatedTime: '2025-10-27 17:36:39',
    UpdatedTime: '2025-10-27 17:36:40',
    CategoryTags: [],
    Classification: null,
    TosStorageClass: 'STANDARD',
    DynamicRange: 'SDR',
    OuterPosterUrl:
      'https://vod-fe-test-aideo-img.byte-test.com/aideo-dev/o8Ir2ejPffnqppYJfpGvQhKzGY30hfjKEAyXSZ~tplv-vod-noop.image',
    FileType: 'video',
    StoreUri: 'aideo-dev/split_55.mp4',
    Md5: 'ff63829f39ab4806b25c1f7f5c5ee44a',
    VodUploadSource: 'upload',
    BlockStatus: '',
    HlsMediaSize: 0,
    MainPlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/split_55.mp4?auth_key=1772272346-90cac36df3a74bd691c242f175e4368f-0-2bcfc5c3c4e30fe83267ef2b7838b7e4',
    BackupPlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/split_55.mp4?auth_key=1772272346-d46b522ab9af455cb4784120b4539e63-0-b14aa531eeed7b82d51b5de48eae6be6',
    Status: 1,
    PlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/split_55.mp4?auth_key=1772272346-90cac36df3a74bd691c242f175e4368f-0-2bcfc5c3c4e30fe83267ef2b7838b7e4',
  },
  v02bffg10064d3vjq82ljhtejm9u1uog: {
    Title: 'split_34.mp4',
    Vid: 'v02bffg10064d3vjq82ljhtejm9u1uog',
    Filename: 'split_34.mp4',
    PublishStatus: 'Published',
    Duration: 4.16,
    Codec: 'h264',
    Height: 1920,
    Width: 1080,
    Format: 'MP4',
    Size: 1941364,
    Bitrate: 3733392,
    Tags: [],
    Description: '',
    PosterUrl:
      'https://console-image-cn.volcvod.com/aideo-dev/oQPBzQvgf6RLi4ZPkmZ1E6ff7CSxdZ0IfIVXB9~noop.jpeg?sign=1769680468-r0-u0-36976857e53ad4cb07491c6daf5eed3b',
    PlayInfo: {
      MainPlayUrl:
        'https://vod-fe-test-aideo.byte-test.com/split_34.mp4?auth_key=1772272468-3979f8e0de514b1cb865c88283ec4f0b-0-fd6991eb6cec50e47f90765478d8e52b',
      BackupPlayUrl:
        'https://vod-fe-test-aideo.byte-test.com/split_34.mp4?auth_key=1772272468-000f04184eaa497986e330d169e383f4-0-baa402352f6bdb71c30f9560e123cd3f',
      Status: 1,
    },
    PosterInfo: {
      MainPosterUri: 'aideo-dev/oQPBzQvgf6RLi4ZPkmZ1E6ff7CSxdZ0IfIVXB9',
      BackupPosterUris: [],
      MainPosterInfo: {
        PosterUri: 'aideo-dev/oQPBzQvgf6RLi4ZPkmZ1E6ff7CSxdZ0IfIVXB9',
        PosterUrl:
          'https://console-image-cn.volcvod.com/aideo-dev/oQPBzQvgf6RLi4ZPkmZ1E6ff7CSxdZ0IfIVXB9~noop.jpeg?sign=1769680468-r0-u0-36976857e53ad4cb07491c6daf5eed3b',
      },
      BackupPosterInfo: [],
    },
    CreatedTime: '2025-10-27 17:36:37',
    UpdatedTime: '2025-10-27 17:36:38',
    CategoryTags: [],
    Classification: null,
    TosStorageClass: 'STANDARD',
    DynamicRange: 'SDR',
    OuterPosterUrl:
      'https://vod-fe-test-aideo-img.byte-test.com/aideo-dev/oQPBzQvgf6RLi4ZPkmZ1E6ff7CSxdZ0IfIVXB9~tplv-vod-noop.image',
    FileType: 'video',
    StoreUri: 'aideo-dev/split_34.mp4',
    Md5: '60eafceab73d06a6325aee49bf8786c5',
    VodUploadSource: 'upload',
    BlockStatus: '',
    HlsMediaSize: 0,
    MainPlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/split_34.mp4?auth_key=1772272468-3979f8e0de514b1cb865c88283ec4f0b-0-fd6991eb6cec50e47f90765478d8e52b',
    BackupPlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/split_34.mp4?auth_key=1772272468-000f04184eaa497986e330d169e383f4-0-baa402352f6bdb71c30f9560e123cd3f',
    Status: 1,
    PlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/split_34.mp4?auth_key=1772272468-3979f8e0de514b1cb865c88283ec4f0b-0-fd6991eb6cec50e47f90765478d8e52b',
  },
  v02bffg10064d3vjq92ljhtbribb9sq0: {
    Title: 'split_50.mp4',
    Vid: 'v02bffg10064d3vjq92ljhtbribb9sq0',
    Filename: 'split_50.mp4',
    PublishStatus: 'Published',
    Duration: 1.88,
    Codec: 'h264',
    Height: 1920,
    Width: 1080,
    Format: 'MP4',
    Size: 342910,
    Bitrate: 1459191,
    Tags: [],
    Description: '',
    PosterUrl:
      'https://console-image-cn.volcvod.com/aideo-dev/ocCC20RgflzxMErPZkISzVZ26fL7fCfvUQTc7Q~noop.jpeg?sign=1769680468-r0-u0-59379a5ce3341cf7f631554f76635028',
    PlayInfo: {
      MainPlayUrl:
        'https://vod-fe-test-aideo.byte-test.com/split_50.mp4?auth_key=1772272468-7bd7243682014223aade44f3bca75f50-0-d960729404fbff5d8e6559b380effe9d',
      BackupPlayUrl:
        'https://vod-fe-test-aideo.byte-test.com/split_50.mp4?auth_key=1772272468-9a152c38a2f14a2e90fec25c5c52f9c7-0-0722973efc9b87c6b053b00c19a33f04',
      Status: 1,
    },
    PosterInfo: {
      MainPosterUri: 'aideo-dev/ocCC20RgflzxMErPZkISzVZ26fL7fCfvUQTc7Q',
      BackupPosterUris: [],
      MainPosterInfo: {
        PosterUri: 'aideo-dev/ocCC20RgflzxMErPZkISzVZ26fL7fCfvUQTc7Q',
        PosterUrl:
          'https://console-image-cn.volcvod.com/aideo-dev/ocCC20RgflzxMErPZkISzVZ26fL7fCfvUQTc7Q~noop.jpeg?sign=1769680468-r0-u0-59379a5ce3341cf7f631554f76635028',
      },
      BackupPosterInfo: [],
    },
    CreatedTime: '2025-10-27 17:36:37',
    UpdatedTime: '2025-10-27 17:36:38',
    CategoryTags: [],
    Classification: null,
    TosStorageClass: 'STANDARD',
    DynamicRange: 'SDR',
    OuterPosterUrl:
      'https://vod-fe-test-aideo-img.byte-test.com/aideo-dev/ocCC20RgflzxMErPZkISzVZ26fL7fCfvUQTc7Q~tplv-vod-noop.image',
    FileType: 'video',
    StoreUri: 'aideo-dev/split_50.mp4',
    Md5: '4ae2cfe920f9b0eb7c999e03404326cd',
    VodUploadSource: 'upload',
    BlockStatus: '',
    HlsMediaSize: 0,
    MainPlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/split_50.mp4?auth_key=1772272468-7bd7243682014223aade44f3bca75f50-0-d960729404fbff5d8e6559b380effe9d',
    BackupPlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/split_50.mp4?auth_key=1772272468-9a152c38a2f14a2e90fec25c5c52f9c7-0-0722973efc9b87c6b053b00c19a33f04',
    Status: 1,
    PlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/split_50.mp4?auth_key=1772272468-7bd7243682014223aade44f3bca75f50-0-d960729404fbff5d8e6559b380effe9d',
  },
  v02bffg10064d3vjq92ljhtbffh24lsg: {
    Title: 'split_51.mp4',
    Vid: 'v02bffg10064d3vjq92ljhtbffh24lsg',
    Filename: 'split_51.mp4',
    PublishStatus: 'Published',
    Duration: 1.8,
    Codec: 'h264',
    Height: 1920,
    Width: 1080,
    Format: 'MP4',
    Size: 738919,
    Bitrate: 3284084,
    Tags: [],
    Description: '',
    PosterUrl:
      'https://console-image-cn.volcvod.com/aideo-dev/oUAjjfHbzEInfII3ZepERSpXzfQk8vkhxyq12e~noop.jpeg?sign=1769680524-r0-u0-94ef3ca5b9c06c89b12713ebefb63344',
    PlayInfo: {
      MainPlayUrl:
        'https://vod-fe-test-aideo.byte-test.com/split_51.mp4?auth_key=1772272524-b06b686dcce74b2891bb06ae2edeb7ce-0-672058b16448c451383fd384b5b3d8c0',
      BackupPlayUrl:
        'https://vod-fe-test-aideo.byte-test.com/split_51.mp4?auth_key=1772272524-e817fd90cf3d48bfbc14eb9a8858c832-0-62f3dd435837f0fd222386fa1d58c8f2',
      Status: 1,
    },
    PosterInfo: {
      MainPosterUri: 'aideo-dev/oUAjjfHbzEInfII3ZepERSpXzfQk8vkhxyq12e',
      BackupPosterUris: [],
      MainPosterInfo: {
        PosterUri: 'aideo-dev/oUAjjfHbzEInfII3ZepERSpXzfQk8vkhxyq12e',
        PosterUrl:
          'https://console-image-cn.volcvod.com/aideo-dev/oUAjjfHbzEInfII3ZepERSpXzfQk8vkhxyq12e~noop.jpeg?sign=1769680524-r0-u0-94ef3ca5b9c06c89b12713ebefb63344',
      },
      BackupPosterInfo: [],
    },
    CreatedTime: '2025-10-27 17:36:39',
    UpdatedTime: '2025-10-27 17:36:40',
    CategoryTags: [],
    Classification: null,
    TosStorageClass: 'STANDARD',
    DynamicRange: 'SDR',
    OuterPosterUrl:
      'https://vod-fe-test-aideo-img.byte-test.com/aideo-dev/oUAjjfHbzEInfII3ZepERSpXzfQk8vkhxyq12e~tplv-vod-noop.image',
    FileType: 'video',
    StoreUri: 'aideo-dev/split_51.mp4',
    Md5: '8d66ebf6ff44d7fe9331e1c8ce5386d7',
    VodUploadSource: 'upload',
    BlockStatus: '',
    HlsMediaSize: 0,
    MainPlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/split_51.mp4?auth_key=1772272524-b06b686dcce74b2891bb06ae2edeb7ce-0-672058b16448c451383fd384b5b3d8c0',
    BackupPlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/split_51.mp4?auth_key=1772272524-e817fd90cf3d48bfbc14eb9a8858c832-0-62f3dd435837f0fd222386fa1d58c8f2',
    Status: 1,
    PlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/split_51.mp4?auth_key=1772272524-b06b686dcce74b2891bb06ae2edeb7ce-0-672058b16448c451383fd384b5b3d8c0',
  },
  v02bffg10064d3vjq9aljht0oe413p20: {
    Title: 'split_54.mp4',
    Vid: 'v02bffg10064d3vjq9aljht0oe413p20',
    Filename: 'split_54.mp4',
    PublishStatus: 'Published',
    Duration: 2.88,
    Codec: 'h264',
    Height: 1920,
    Width: 1080,
    Format: 'MP4',
    Size: 711940,
    Bitrate: 1977611,
    Tags: [],
    Description: '',
    PosterUrl:
      'https://console-image-cn.volcvod.com/aideo-dev/ogfhfJtgz0XHffHyA2ujQKCPnIeRpGj8YEEqIk~noop.jpeg?sign=1769680580-r0-u0-e3f4226242978624c400b11c739d2ff5',
    PlayInfo: {
      MainPlayUrl:
        'https://vod-fe-test-aideo.byte-test.com/split_54.mp4?auth_key=1772272580-75fb679fe71b479fa7f7481719dd0762-0-94faac1a6a10f00a69bf53c0c5815c27',
      BackupPlayUrl:
        'https://vod-fe-test-aideo.byte-test.com/split_54.mp4?auth_key=1772272580-8ce87a5c9da849808fe27181fdedd916-0-0b1de01412de5a34cced5b43974259ec',
      Status: 1,
    },
    PosterInfo: {
      MainPosterUri: 'aideo-dev/ogfhfJtgz0XHffHyA2ujQKCPnIeRpGj8YEEqIk',
      BackupPosterUris: [],
      MainPosterInfo: {
        PosterUri: 'aideo-dev/ogfhfJtgz0XHffHyA2ujQKCPnIeRpGj8YEEqIk',
        PosterUrl:
          'https://console-image-cn.volcvod.com/aideo-dev/ogfhfJtgz0XHffHyA2ujQKCPnIeRpGj8YEEqIk~noop.jpeg?sign=1769680580-r0-u0-e3f4226242978624c400b11c739d2ff5',
      },
      BackupPosterInfo: [],
    },
    CreatedTime: '2025-10-27 17:36:39',
    UpdatedTime: '2025-10-27 17:36:40',
    CategoryTags: [],
    Classification: null,
    TosStorageClass: 'STANDARD',
    DynamicRange: 'SDR',
    OuterPosterUrl:
      'https://vod-fe-test-aideo-img.byte-test.com/aideo-dev/ogfhfJtgz0XHffHyA2ujQKCPnIeRpGj8YEEqIk~tplv-vod-noop.image',
    FileType: 'video',
    StoreUri: 'aideo-dev/split_54.mp4',
    Md5: '6caa32ddf9decca3382cde69e12b55b2',
    VodUploadSource: 'upload',
    BlockStatus: '',
    HlsMediaSize: 0,
    MainPlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/split_54.mp4?auth_key=1772272580-75fb679fe71b479fa7f7481719dd0762-0-94faac1a6a10f00a69bf53c0c5815c27',
    BackupPlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/split_54.mp4?auth_key=1772272580-8ce87a5c9da849808fe27181fdedd916-0-0b1de01412de5a34cced5b43974259ec',
    Status: 1,
    PlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/split_54.mp4?auth_key=1772272580-75fb679fe71b479fa7f7481719dd0762-0-94faac1a6a10f00a69bf53c0c5815c27',
  },
  v02bffg10064d3vjq9aljht6ujf4ij5g: {
    Title: 'split_55.mp4',
    Vid: 'v02bffg10064d3vjq9aljht6ujf4ij5g',
    Filename: 'split_55.mp4',
    PublishStatus: 'Published',
    Duration: 2.28,
    Codec: 'h264',
    Height: 1920,
    Width: 1080,
    Format: 'MP4',
    Size: 1146706,
    Bitrate: 4023529,
    Tags: [],
    Description: '',
    PosterUrl:
      'https://console-image-cn.volcvod.com/aideo-dev/o8Ir2ejPffnqppYJfpGvQhKzGY30hfjKEAyXSZ~noop.jpeg?sign=1769680580-r0-u0-d8c1502261739fd9730253e903aa2636',
    PlayInfo: {
      MainPlayUrl:
        'https://vod-fe-test-aideo.byte-test.com/split_55.mp4?auth_key=1772272580-f2724df6d3ac400c91b07e6ab5870b71-0-1ec6c65c08e93163d43cd200e62d38a4',
      BackupPlayUrl:
        'https://vod-fe-test-aideo.byte-test.com/split_55.mp4?auth_key=1772272580-e5785e051f3d4bd49e3b81cde920f8d5-0-070df00d7394722ea0a28677037304c0',
      Status: 1,
    },
    PosterInfo: {
      MainPosterUri: 'aideo-dev/o8Ir2ejPffnqppYJfpGvQhKzGY30hfjKEAyXSZ',
      BackupPosterUris: [],
      MainPosterInfo: {
        PosterUri: 'aideo-dev/o8Ir2ejPffnqppYJfpGvQhKzGY30hfjKEAyXSZ',
        PosterUrl:
          'https://console-image-cn.volcvod.com/aideo-dev/o8Ir2ejPffnqppYJfpGvQhKzGY30hfjKEAyXSZ~noop.jpeg?sign=1769680580-r0-u0-d8c1502261739fd9730253e903aa2636',
      },
      BackupPosterInfo: [],
    },
    CreatedTime: '2025-10-27 17:36:39',
    UpdatedTime: '2025-10-27 17:36:40',
    CategoryTags: [],
    Classification: null,
    TosStorageClass: 'STANDARD',
    DynamicRange: 'SDR',
    OuterPosterUrl:
      'https://vod-fe-test-aideo-img.byte-test.com/aideo-dev/o8Ir2ejPffnqppYJfpGvQhKzGY30hfjKEAyXSZ~tplv-vod-noop.image',
    FileType: 'video',
    StoreUri: 'aideo-dev/split_55.mp4',
    Md5: 'ff63829f39ab4806b25c1f7f5c5ee44a',
    VodUploadSource: 'upload',
    BlockStatus: '',
    HlsMediaSize: 0,
    MainPlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/split_55.mp4?auth_key=1772272580-f2724df6d3ac400c91b07e6ab5870b71-0-1ec6c65c08e93163d43cd200e62d38a4',
    BackupPlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/split_55.mp4?auth_key=1772272580-e5785e051f3d4bd49e3b81cde920f8d5-0-070df00d7394722ea0a28677037304c0',
    Status: 1,
    PlayUrl:
      'https://vod-fe-test-aideo.byte-test.com/split_55.mp4?auth_key=1772272580-f2724df6d3ac400c91b07e6ab5870b71-0-1ec6c65c08e93163d43cd200e62d38a4',
  },
}

// 未匹配到 Vid 时的默认返回值
const MOCK_GET_VIDEO_INFO_DEFAULT = {
  Duration: 10,
  PlayUrl: 'https://example.com/mock-video.mp4',
  PosterUrl: 'https://example.com/mock-poster.jpg',
  Width: 1920,
  Height: 1080,
}

/**
 * 根据 params.Vid 从 map 中取 mock 视频信息，无匹配则返回默认
 * @param {{ Vid?: string; Space?: string }} params
 * @returns {object}
 */
export function getMockVideoInfoByParams(params) {
  const vid = params?.Vid
  const matched = vid && MOCK_GET_VIDEO_INFO_BY_VID[vid]
  return matched ? { ...matched } : { ...MOCK_GET_VIDEO_INFO_DEFAULT }
}

// mGetMaterial 在 image 时被调，期望返回 MaterialSet.MaterialInfos[0].MaterialBasicInfo
export const MOCK_M_GET_MATERIAL = {
  MaterialSet: {
    MaterialInfos: [
      {
        MaterialBasicInfo: {
          Width: 1920,
          Height: 1080,
          PlayUrl: 'https://example.com/mock-image.jpg',
          PosterUrl: 'https://example.com/mock-image.jpg',
        },
      },
    ],
  },
}
/**
 * MOCK_TRACK：仅作 Track 结构参考（Type、Source、TargetTime、Extra、UserData 等字段形状）。
 * 其中的 url、auth_key 等为 MOCK 示例，不得直接用于预览。
 * 预览页必须从 output/review_import_data.json 导入，track 内的 URL 需为流水线产出的真实可播放链接。
 */
export const MOCK_TRACK = [
  [
    {
      ID: 'ucirqys1sp8',
      Type: 'video',
      Source: 'vid://v02bffg10064d3vjq9aljht6ujf4ij5g',
      UserData: {
        id: 'element19c4becc82b10000000001',
        name: 'split_55.mp4',
        source: 'vid://v02bffg10064d3vjq9aljht6ujf4ij5g',
        type: 'video',
        url: 'https://vod-fe-test-aideo.byte-test.com/split_55.mp4?auth_key=1774870443-fcc8c01ff36b46f8b44547ebd0058cac-0-e23f1a65b3e3eaf49a39f0c299128f4f',
        width: 1080,
        height: 1920,
        aspectRatio: 1080 / 1920,
        originalDuration: 2.28,
        poster:
          'https://console-image-cn.volcvod.com/aideo-dev/o8Ir2ejPffnqppYJfpGvQhKzGY30hfjKEAyXSZ~noop.jpeg?sign=1772278443-r0-u0-67dd3d85283b997c13ac9757d3f6aa00',
      },
      TargetTime: [0, 2280],
      UserData: {
        id: 'element19c1e87b2bf10000000008',
        source: 'loki://1179433',
        url: 'https://lf26-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/4f6ef1bb3bd730dc6dd80ad5f5f5bb10',
        fontFamily: '站酷仓耳渔阳体',
        fontTypeUrl:
          'https://lf5-hl-hw-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/098d75dd0be7cc0f303b12e3cd2b918e',
        fontTypeRef: '1187223',
        type: 'text',
        textType: '',
        trackStyle: {
          backgroundColor: 'green',
          color: 'red',
          fontSize: 14,
          borderRadius: '4px',
        },
      },
    },
  ],
  [
    {
      ID: '8epztxp6y64',
      Type: 'video',
      Source: 'vid://v02bffg10064d3vjq9aljht0oe413p20',
      UserData: {
        id: 'element19ca40717641000000000f',
        name: 'split_54.mp4',
        source: 'vid://v02bffg10064d3vjq9aljht0oe413p20',
        type: 'video',
        url: 'https://vod-fe-test-aideo.byte-test.com/split_54.mp4?auth_key=1774870443-f0fbe33b74af479e907768b22749391f-0-e211911e48e0e7d56f47525853d5fa1b',
        width: 1080,
        height: 1920,
        aspectRatio: 1080 / 1920,
        originalDuration: 2.88,
        poster:
          'https://console-image-cn.volcvod.com/aideo-dev/ogfhfJtgz0XHffHyA2ujQKCPnIeRpGj8YEEqIk~noop.jpeg?sign=1772278443-r0-u0-0f12d033a0cf7a661ccc5d820bd5a3c6',
      },
      TargetTime: [1050, 3930],
      Extra: [
        {
          ID: '8epztxp6y64_transform',
          Type: 'transform',
          PosX: 656,
          PosY: 0,
          ScaleX: 1,
          ScaleY: 1,
          Width: 608,
          Height: 1080,
          Rotation: 0,
          FlipX: false,
          FlipY: false,
          Alpha: 1,
          UserData: {
            id: 'element19ca40717641000000000f',
            name: 'split_54.mp4',
            source: 'vid://v02bffg10064d3vjq9aljht0oe413p20',
            type: 'video',
            url: 'https://vod-fe-test-aideo.byte-test.com/split_54.mp4?auth_key=1774870443-f0fbe33b74af479e907768b22749391f-0-e211911e48e0e7d56f47525853d5fa1b',
            width: 1080,
            height: 1920,
            originalDuration: 2.88,
            poster:
              'https://console-image-cn.volcvod.com/aideo-dev/ogfhfJtgz0XHffHyA2ujQKCPnIeRpGj8YEEqIk~noop.jpeg?sign=1772278443-r0-u0-0f12d033a0cf7a661ccc5d820bd5a3c6',
          },
        },
        {
          ID: '8epztxp6y64_eq',
          Type: 'equalizer',
          TargetTime: [0, 2880],
          Brightness: 0,
          Contrast: 0,
          Saturation: 0,
          Sharpen: 0,
          Highlight: 0,
          Temperature: 0,
          Tone: 0,
          UserData: {
            id: 'element19ca40717641000000000f',
            name: 'split_54.mp4',
            source: 'vid://v02bffg10064d3vjq9aljht0oe413p20',
            type: 'video',
            url: 'https://vod-fe-test-aideo.byte-test.com/split_54.mp4?auth_key=1774870443-f0fbe33b74af479e907768b22749391f-0-e211911e48e0e7d56f47525853d5fa1b',
            width: 1080,
            height: 1920,
            originalDuration: 2.88,
            poster:
              'https://console-image-cn.volcvod.com/aideo-dev/ogfhfJtgz0XHffHyA2ujQKCPnIeRpGj8YEEqIk~noop.jpeg?sign=1772278443-r0-u0-0f12d033a0cf7a661ccc5d820bd5a3c6',
          },
        },
        {
          ID: '8epztxp6y64_volume',
          Type: 'a_volume',
          Volume: 1,
          UserData: {
            id: 'element19ca40717641000000000f',
            name: 'split_54.mp4',
            source: 'vid://v02bffg10064d3vjq9aljht0oe413p20',
            type: 'video',
            url: 'https://vod-fe-test-aideo.byte-test.com/split_54.mp4?auth_key=1774870443-f0fbe33b74af479e907768b22749391f-0-e211911e48e0e7d56f47525853d5fa1b',
            width: 1080,
            height: 1920,
            originalDuration: 2.88,
            poster:
              'https://console-image-cn.volcvod.com/aideo-dev/ogfhfJtgz0XHffHyA2ujQKCPnIeRpGj8YEEqIk~noop.jpeg?sign=1772278443-r0-u0-0f12d033a0cf7a661ccc5d820bd5a3c6',
          },
        },
        {
          ID: '8epztxp6y64_trim',
          Type: 'trim',
          StartTime: 0,
          EndTime: 2880,
          UserData: {
            id: 'element19ca40717641000000000f',
            name: 'split_54.mp4',
            source: 'vid://v02bffg10064d3vjq9aljht0oe413p20',
            type: 'video',
            url: 'https://vod-fe-test-aideo.byte-test.com/split_54.mp4?auth_key=1774870443-f0fbe33b74af479e907768b22749391f-0-e211911e48e0e7d56f47525853d5fa1b',
            width: 1080,
            height: 1920,
            originalDuration: 2.88,
            poster:
              'https://console-image-cn.volcvod.com/aideo-dev/ogfhfJtgz0XHffHyA2ujQKCPnIeRpGj8YEEqIk~noop.jpeg?sign=1772278443-r0-u0-0f12d033a0cf7a661ccc5d820bd5a3c6',
          },
        },
        {
          ID: '8epztxp6y64_speed',
          Type: 'speed',
          Speed: 1,
          UserData: {
            id: 'element19ca40717641000000000f',
            name: 'split_54.mp4',
            source: 'vid://v02bffg10064d3vjq9aljht0oe413p20',
            type: 'video',
            url: 'https://vod-fe-test-aideo.byte-test.com/split_54.mp4?auth_key=1774870443-f0fbe33b74af479e907768b22749391f-0-e211911e48e0e7d56f47525853d5fa1b',
            width: 1080,
            height: 1920,
            originalDuration: 2.88,
            poster:
              'https://console-image-cn.volcvod.com/aideo-dev/ogfhfJtgz0XHffHyA2ujQKCPnIeRpGj8YEEqIk~noop.jpeg?sign=1772278443-r0-u0-0f12d033a0cf7a661ccc5d820bd5a3c6',
          },
        },
      ],
    },
  ],
  [
    {
      ID: '2qkr0vwsu98',
      Type: 'video',
      Source: 'vid://v02bffg10064d3vjq82ljhtejm9u1uog',
      UserData: {
        id: 'element19ca4085cb110000000016',
        name: 'split_34.mp4',
        source: 'vid://v02bffg10064d3vjq82ljhtejm9u1uog',
        type: 'video',
        url: 'https://vod-fe-test-aideo.byte-test.com/split_34.mp4?auth_key=1774870443-3653567a0ef34b29b6f9c24bab42caad-0-1d242e5ff0863ed5e8bb7a5375858337',
        width: 1080,
        height: 1920,
        originalDuration: 4.16,
        poster:
          'https://console-image-cn.volcvod.com/aideo-dev/oQPBzQvgf6RLi4ZPkmZ1E6ff7CSxdZ0IfIVXB9~noop.jpeg?sign=1772278443-r0-u0-4966375c109791c89acff05c8e83a6ba',
      },
      TargetTime: [2640, 6800],
      Extra: [
        {
          ID: '2qkr0vwsu98_transform',
          Type: 'transform',
          PosX: 656,
          PosY: 0,
          ScaleX: 1,
          ScaleY: 1,
          Width: 608,
          Height: 1080,
          Rotation: 0,
          FlipX: false,
          FlipY: false,
          Alpha: 1,
          UserData: {
            id: 'element19ca4085cb110000000016',
            name: 'split_34.mp4',
            source: 'vid://v02bffg10064d3vjq82ljhtejm9u1uog',
            type: 'video',
            url: 'https://vod-fe-test-aideo.byte-test.com/split_34.mp4?auth_key=1774870443-3653567a0ef34b29b6f9c24bab42caad-0-1d242e5ff0863ed5e8bb7a5375858337',
            width: 1080,
            height: 1920,
            originalDuration: 4.16,
            poster:
              'https://console-image-cn.volcvod.com/aideo-dev/oQPBzQvgf6RLi4ZPkmZ1E6ff7CSxdZ0IfIVXB9~noop.jpeg?sign=1772278443-r0-u0-4966375c109791c89acff05c8e83a6ba',
          },
        },
        {
          ID: '2qkr0vwsu98_eq',
          Type: 'equalizer',
          TargetTime: [0, 4160],
          Brightness: 0,
          Contrast: 0,
          Saturation: 0,
          Sharpen: 0,
          Highlight: 0,
          Temperature: 0,
          Tone: 0,
          UserData: {
            id: 'element19ca4085cb110000000016',
            name: 'split_34.mp4',
            source: 'vid://v02bffg10064d3vjq82ljhtejm9u1uog',
            type: 'video',
            url: 'https://vod-fe-test-aideo.byte-test.com/split_34.mp4?auth_key=1774870443-3653567a0ef34b29b6f9c24bab42caad-0-1d242e5ff0863ed5e8bb7a5375858337',
            width: 1080,
            height: 1920,
            originalDuration: 4.16,
            poster:
              'https://console-image-cn.volcvod.com/aideo-dev/oQPBzQvgf6RLi4ZPkmZ1E6ff7CSxdZ0IfIVXB9~noop.jpeg?sign=1772278443-r0-u0-4966375c109791c89acff05c8e83a6ba',
          },
        },
        {
          ID: '2qkr0vwsu98_volume',
          Type: 'a_volume',
          Volume: 1,
          UserData: {
            id: 'element19ca4085cb110000000016',
            name: 'split_34.mp4',
            source: 'vid://v02bffg10064d3vjq82ljhtejm9u1uog',
            type: 'video',
            url: 'https://vod-fe-test-aideo.byte-test.com/split_34.mp4?auth_key=1774870443-3653567a0ef34b29b6f9c24bab42caad-0-1d242e5ff0863ed5e8bb7a5375858337',
            width: 1080,
            height: 1920,
            originalDuration: 4.16,
            poster:
              'https://console-image-cn.volcvod.com/aideo-dev/oQPBzQvgf6RLi4ZPkmZ1E6ff7CSxdZ0IfIVXB9~noop.jpeg?sign=1772278443-r0-u0-4966375c109791c89acff05c8e83a6ba',
          },
        },
        {
          ID: '2qkr0vwsu98_trim',
          Type: 'trim',
          StartTime: 0,
          EndTime: 4160,
          UserData: {
            id: 'element19ca4085cb110000000016',
            name: 'split_34.mp4',
            source: 'vid://v02bffg10064d3vjq82ljhtejm9u1uog',
            type: 'video',
            url: 'https://vod-fe-test-aideo.byte-test.com/split_34.mp4?auth_key=1774870443-3653567a0ef34b29b6f9c24bab42caad-0-1d242e5ff0863ed5e8bb7a5375858337',
            width: 1080,
            height: 1920,
            originalDuration: 4.16,
            poster:
              'https://console-image-cn.volcvod.com/aideo-dev/oQPBzQvgf6RLi4ZPkmZ1E6ff7CSxdZ0IfIVXB9~noop.jpeg?sign=1772278443-r0-u0-4966375c109791c89acff05c8e83a6ba',
          },
        },
        {
          ID: '2qkr0vwsu98_speed',
          Type: 'speed',
          Speed: 1,
          UserData: {
            id: 'element19ca4085cb110000000016',
            name: 'split_34.mp4',
            source: 'vid://v02bffg10064d3vjq82ljhtejm9u1uog',
            type: 'video',
            url: 'https://vod-fe-test-aideo.byte-test.com/split_34.mp4?auth_key=1774870443-3653567a0ef34b29b6f9c24bab42caad-0-1d242e5ff0863ed5e8bb7a5375858337',
            width: 1080,
            height: 1920,
            originalDuration: 4.16,
            poster:
              'https://console-image-cn.volcvod.com/aideo-dev/oQPBzQvgf6RLi4ZPkmZ1E6ff7CSxdZ0IfIVXB9~noop.jpeg?sign=1772278443-r0-u0-4966375c109791c89acff05c8e83a6ba',
          },
        },
      ],
    },
  ],
]
export const MOCK_TRACK2 = [
  [
    {
      ID: 'h38fporyk3l',
      Type: 'video',
      Source: 'vid://v02bffg10064d3vjq9aljht0oe413p20',
      UserData: {
        id: 'element19c08a8b7f81000000000f',
        name: 'split_54.mp4',
        source: 'vid://v02bffg10064d3vjq9aljht0oe413p20',
        type: 'video',
        width: 1080,
        height: 1920,
        originalDuration: 2.88,
        url: 'https://vod-fe-test-aideo.byte-test.com/split_54.mp4?auth_key=1772272580-75fb679fe71b479fa7f7481719dd0762-0-94faac1a6a10f00a69bf53c0c5815c27',
        poster:
          'https://console-image-cn.volcvod.com/aideo-dev/ogfhfJtgz0XHffHyA2ujQKCPnIeRpGj8YEEqIk~noop.jpeg?sign=1769680580-r0-u0-e3f4226242978624c400b11c739d2ff5',
      },
      TargetTime: [0, 2880],
    },
  ],
  [
    {
      ID: 'va07tfjs8tr',
      Type: 'video',
      Source: 'vid://v02bffg10064d3vjq9aljht6ujf4ij5g',
      UserData: {
        id: 'element19c093370e41000000000f',
        name: 'split_55.mp4',
        source: 'vid://v02bffg10064d3vjq9aljht6ujf4ij5g',
        type: 'video',
        url: 'https://vod-fe-test-aideo.byte-test.com/split_55.mp4?auth_key=1772272580-f2724df6d3ac400c91b07e6ab5870b71-0-1ec6c65c08e93163d43cd200e62d38a4',
        width: 1080,
        height: 1920,
        originalDuration: 2.28,
        poster:
          'https://console-image-cn.volcvod.com/aideo-dev/o8Ir2ejPffnqppYJfpGvQhKzGY30hfjKEAyXSZ~noop.jpeg?sign=1769680580-r0-u0-d8c1502261739fd9730253e903aa2636',
      },
      TargetTime: [900, 3180],
    },
  ],
]
/** 模拟删除轨道：仅保留第 1 条轨道（用于 demo 按钮「删除轨道」在仅剩 1 条时恢复用） */
export const MOCK_TRACK_DEL = [MOCK_TRACK[0]]

/** 新增一条轨道时用的单个视频片段模板（后端格式），用于 demo「增加轨道」在现有轨道上追加一条 */
export const MOCK_NEW_TRACK_ELEMENT = {
  ID: 'mock_add_track_element_1',
  Type: 'video',
  Source: 'vid://v02bffg10064d3vjq9aljht0oe413p20',
  UserData: {
    id: 'mock_add_element_1',
    name: 'split_54.mp4',
    source: 'vid://v02bffg10064d3vjq9aljht0oe413p20',
    type: 'video',
    width: 1080,
    height: 1920,
    originalDuration: 2.88,
    url: 'https://vod-fe-test-aideo.byte-test.com/split_54.mp4?auth_key=1772272580-75fb679fe71b479fa7f7481719dd0762-0-94faac1a6a10f00a69bf53c0c5815c27',
    poster:
      'https://console-image-cn.volcvod.com/aideo-dev/ogfhfJtgz0XHffHyA2ujQKCPnIeRpGj8YEEqIk~noop.jpeg?sign=1769680580-r0-u0-e3f4226242978624c400b11c739d2ff5',
  },
  TargetTime: [4000, 6880],
}

export const remark_TRACK_ELEMENT = [
  // 一条轨道（Track），数组内为该轨道上的元素列表
  [
    {
      // 元素唯一 ID，业务侧用于关联 getVideoFrame 等
      ID: 'kbcgoc952m',
      TrackId: 'track1',
      // 元素类型：video | audio | image | text | effect | sticker
      Type: 'video',
      // 素材来源标识，视频/音频为 vid://xxx，图片为 mid://xxx
      Source: 'vid://v02bffg10064d3vjq9aljht0oe413p20',
      // 业务侧透传数据，含展示用 name、播放 url、封面 poster、原始宽高与时长等
      UserData: {
        id: 'element19c08a8b7f81000000000f',
        name: 'split_54.mp4',
        source: 'vid://v02bffg10064d3vjq9aljht0oe413p20',
        type: 'video',
        width: 1080,
        height: 1920,
        originalDuration: 2.88,
        url: 'https://vod-fe-test-aideo.byte-test.com/split_54.mp4?auth_key=1772279732-bf753f15aba547e99f8e4ecae8b5217d-0-1b9560eb6b509e1b2371f6fca04227e5',
        poster:
          'https://console-image-cn.volcvod.com/aideo-dev/ogfhfJtgz0XHffHyA2ujQKCPnIeRpGj8YEEqIk~noop.jpeg?sign=1769687732-r0-u0-79503ff3dc915c02d8dc9d0ef05944a6',
      },
      // 该元素在时间轴上的起止时间 [开始ms, 结束ms]
      TargetTime: [0, 1704],
      // 该元素上的滤镜/特效列表（transform、调色、音量、裁剪、倍速等）
      Extra: [
        {
          ID: 'kbcgoc952m_transform',
          Type: 'transform',
          PosX: 656, // 画布内 X
          PosY: 3, // 画布内 X
          ScaleX: 1,
          ScaleY: 1,
          Width: 608,
          Height: 1080,
          Rotation: 14, // 旋转角度（度）
          FlipX: false,
          FlipY: false,
          Alpha: 1, // 不透明度 0–1
          UserData: {
            id: 'element19c08a8b7f81000000000f',
            name: 'split_54.mp4',
            source: 'vid://v02bffg10064d3vjq9aljht0oe413p20',
            type: 'video',
            width: 1080,
            height: 1920,
            originalDuration: 2.88,
            url: 'https://vod-fe-test-aideo.byte-test.com/split_54.mp4?auth_key=1772279732-bf753f15aba547e99f8e4ecae8b5217d-0-1b9560eb6b509e1b2371f6fca04227e5',
            poster:
              'https://console-image-cn.volcvod.com/aideo-dev/ogfhfJtgz0XHffHyA2ujQKCPnIeRpGj8YEEqIk~noop.jpeg?sign=1769687732-r0-u0-79503ff3dc915c02d8dc9d0ef05944a6',
          },
        },
        {
          ID: 'kbcgoc952m_volume',
          Type: 'a_volume',
          Volume: 0.51, // 音量 0–1
          UserData: {
            id: 'element19c08a8b7f81000000000f',
            name: 'split_54.mp4',
            source: 'vid://v02bffg10064d3vjq9aljht0oe413p20',
            type: 'video',
            width: 1080,
            height: 1920,
            originalDuration: 2.88,
            url: 'https://vod-fe-test-aideo.byte-test.com/split_54.mp4?auth_key=1772279732-bf753f15aba547e99f8e4ecae8b5217d-0-1b9560eb6b509e1b2371f6fca04227e5',
            poster:
              'https://console-image-cn.volcvod.com/aideo-dev/ogfhfJtgz0XHffHyA2ujQKCPnIeRpGj8YEEqIk~noop.jpeg?sign=1769687732-r0-u0-79503ff3dc915c02d8dc9d0ef05944a6',
          },
        },
        {
          ID: 'kbcgoc952m_trim',
          Type: 'trim',
          StartTime: 0, // 裁剪起始时间 ms（相对原片）
          EndTime: 2880, // 裁剪结束时间 ms（相对原片）
          UserData: {
            id: 'element19c08a8b7f81000000000f',
            name: 'split_54.mp4',
            source: 'vid://v02bffg10064d3vjq9aljht0oe413p20',
            type: 'video',
            width: 1080,
            height: 1920,
            originalDuration: 2.88,
            url: 'https://vod-fe-test-aideo.byte-test.com/split_54.mp4?auth_key=1772279732-bf753f15aba547e99f8e4ecae8b5217d-0-1b9560eb6b509e1b2371f6fca04227e5',
            poster:
              'https://console-image-cn.volcvod.com/aideo-dev/ogfhfJtgz0XHffHyA2ujQKCPnIeRpGj8YEEqIk~noop.jpeg?sign=1769687732-r0-u0-79503ff3dc915c02d8dc9d0ef05944a6',
          },
        },
        {
          ID: 'kbcgoc952m_speed',
          Type: 'speed',
          Speed: 1.69, // 播放倍速，如 1.69 表示 1.69 倍速
          UserData: {
            id: 'element19c08a8b7f81000000000f',
            name: 'split_54.mp4',
            source: 'vid://v02bffg10064d3vjq9aljht0oe413p20',
            type: 'video',
            width: 1080,
            height: 1920,
            originalDuration: 2.88,
            url: 'https://vod-fe-test-aideo.byte-test.com/split_54.mp4?auth_key=1772279732-bf753f15aba547e99f8e4ecae8b5217d-0-1b9560eb6b509e1b2371f6fca04227e5',
            poster:
              'https://console-image-cn.volcvod.com/aideo-dev/ogfhfJtgz0XHffHyA2ujQKCPnIeRpGj8YEEqIk~noop.jpeg?sign=1769687732-r0-u0-79503ff3dc915c02d8dc9d0ef05944a6',
          },
        },
      ],
    },
  ],
]
