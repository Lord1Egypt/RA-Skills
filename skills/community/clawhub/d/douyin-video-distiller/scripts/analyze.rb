#!/usr/bin/env ruby
# frozen_string_literal: true

require 'base64'
require 'json'
require 'net/http'
require 'uri'

DEFAULT_ENDPOINT = 'https://integrate.api.nvidia.com/v1/chat/completions'
DEFAULT_MODEL = 'nvidia/nemotron-3-nano-omni-30b-a3b-reasoning'
TIMEOUT_SECONDS = Integer(ENV.fetch('NVIDIA_TIMEOUT_SECONDS', '600'))
# 请求体上限 25 MB（base64 膨胀约 4/3），给 JSON 外壳留余量，原始文件按 ~18 MB 设限
MAX_RAW_BYTES = Integer(ENV.fetch('NVIDIA_MAX_RAW_BYTES', "#{18 * 1024 * 1024}"))

HELP = <<~TEXT
  用法:
    ruby analyze.rb <图片或视频路径> <中文指令> [--json]

  环境变量:
    NVIDIA_API_KEY     必填。在 https://build.nvidia.com 免费注册后获取
    NVIDIA_MODEL       可选，覆盖默认模型
    NVIDIA_ENDPOINT    可选，覆盖默认端点

  图片示例:
    ruby analyze.rb image.png "请读取图片中的所有文字"

  视频示例:
    ruby analyze.rb video.mp4 "请总结完整视频并列出关键事件"
TEXT

abort(HELP) if ARGV.empty? || ARGV.include?('--help') || ARGV.include?('-h')
json_output = ARGV.delete('--json')
input_path = ARGV.shift
instruction = ARGV.join(' ').strip
abort(HELP) if input_path.nil? || instruction.empty?
abort("输入文件不存在: #{input_path}") unless File.file?(input_path)

video_exts = %w[.mp4 .mov .avi .mkv .webm .m4v .mpeg .mpg]
ext = File.extname(input_path).downcase

mime_by_ext = {
  '.png' => 'image/png', '.jpg' => 'image/jpeg', '.jpeg' => 'image/jpeg',
  '.webp' => 'image/webp', '.gif' => 'image/gif', '.bmp' => 'image/bmp',
  '.mp4' => 'video/mp4', '.mov' => 'video/quicktime', '.avi' => 'video/x-msvideo',
  '.mkv' => 'video/x-matroska', '.webm' => 'video/webm', '.m4v' => 'video/x-m4v',
  '.mpeg' => 'video/mpeg', '.mpg' => 'video/mpeg'
}
mime = mime_by_ext[ext]
abort('不支持的输入格式，请使用图片 PNG/JPEG/WEBP/GIF/BMP 或视频 MP4/MOV/AVI/MKV/WEBM。') unless mime

size = File.size(input_path)
if size > MAX_RAW_BYTES
  abort(<<~MSG)
    文件过大（#{(size / 1048576.0).round(1)} MB，超过 #{(MAX_RAW_BYTES / 1048576.0).round(0)} MB 上限）。
    NVIDIA API 单次请求体上限 25 MB（base64 后）。请先用 FFmpeg 切段压缩再分析，例如：
      ffmpeg -i input.mp4 -ss 0 -t 150 -vf scale=720:-2 -c:v libx264 -crf 32 -c:a aac -b:a 64k seg_00.mp4
    每段约 2-4 MB，逐段调用本脚本分析后合并结果。
  MSG
end

api_key = ENV['NVIDIA_API_KEY']
if api_key.nil? || api_key.strip.empty?
  abort(<<~MSG)
    未找到 NVIDIA_API_KEY。
    1. 打开 https://build.nvidia.com 注册（免费，含免费额度）
    2. 获取 API Key 后设置环境变量：
       Linux/macOS: export NVIDIA_API_KEY="nvapi-xxxx"
       Windows PowerShell: $env:NVIDIA_API_KEY="nvapi-xxxx"
  MSG
end
api_key = api_key.strip

endpoint = URI(ENV.fetch('NVIDIA_ENDPOINT', DEFAULT_ENDPOINT))
model = ENV.fetch('NVIDIA_MODEL', DEFAULT_MODEL)
encoded = Base64.strict_encode64(File.binread(input_path))
content = [{ type: 'text', text: instruction }]
if mime.start_with?('video/')
  # NVIDIA 的 Omni 端点使用视频块时通常要求 video_url；如官方页面指定了别的字段，可通过 NVIDIA_VIDEO_CONTENT_TYPE 覆盖。
  video_type = ENV.fetch('NVIDIA_VIDEO_CONTENT_TYPE', 'video_url')
  content << if video_type == 'video_url'
    { type: 'video_url', video_url: { url: "data:#{mime};base64,#{encoded}" } }
  else
    { type: video_type, video: "data:#{mime};base64,#{encoded}" }
  end
else
  content << { type: 'image_url', image_url: { url: "data:#{mime};base64,#{encoded}" } }
end
payload = {
  model: model,
  messages: [{ role: 'user', content: content }],
  max_tokens: Integer(ENV.fetch('NVIDIA_MAX_TOKENS', '65536')),
  reasoning_budget: Integer(ENV.fetch('NVIDIA_REASONING_BUDGET', '16384')),
  stream: false,
  temperature: Float(ENV.fetch('NVIDIA_TEMPERATURE', '0.6')),
  top_p: Float(ENV.fetch('NVIDIA_TOP_P', '0.95'))
}

request = Net::HTTP::Post.new(endpoint)
request['Authorization'] = "Bearer #{api_key}"
request['Content-Type'] = 'application/json'
request.body = JSON.generate(payload)
http = Net::HTTP.new(endpoint.host, endpoint.port)
http.use_ssl = endpoint.scheme == 'https'
http.open_timeout = TIMEOUT_SECONDS
http.read_timeout = TIMEOUT_SECONDS
http.write_timeout = TIMEOUT_SECONDS if http.respond_to?(:write_timeout=)

begin
  response = http.request(request)
rescue Net::OpenTimeout, Net::ReadTimeout, Net::WriteTimeout
  abort("请求 NVIDIA API 超时（#{TIMEOUT_SECONDS} 秒）。请检查网络、输入文件大小或稍后重试。")
rescue StandardError => e
  abort("请求 NVIDIA API 失败: #{e.class}: #{e.message}")
end

begin
  parsed = JSON.parse(response.body)
rescue JSON::ParserError
  abort("NVIDIA API 返回了无法解析的响应（HTTP #{response.code}）。")
end

unless response.is_a?(Net::HTTPSuccess)
  message = parsed.dig('error', 'message') || parsed['message'] || response.body
  abort("NVIDIA API 请求失败（HTTP #{response.code}）: #{message}")
end

answer = parsed.dig('choices', 0, 'message', 'content')
abort('API 返回成功，但没有找到模型回答。') if answer.nil? || answer.empty?
if json_output
  puts JSON.pretty_generate('model' => parsed['model'] || model, 'answer' => answer, 'usage' => parsed['usage'])
else
  puts answer
end
