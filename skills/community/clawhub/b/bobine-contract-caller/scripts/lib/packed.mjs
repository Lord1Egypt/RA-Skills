import { bytesToHex, hexToBytes } from "./hex.mjs"

class ByteWriter {
  #chunks = []

  writeUint8(value) {
    this.#chunks.push(Uint8Array.of(value & 0xff))
  }

  writeUint32(value) {
    const bytes = new Uint8Array(4)
    new DataView(bytes.buffer).setUint32(0, value, true)
    this.#chunks.push(bytes)
  }

  writeFloat64(value) {
    const bytes = new Uint8Array(8)
    new DataView(bytes.buffer).setFloat64(0, value, true)
    this.#chunks.push(bytes)
  }

  writeBytes(bytes) {
    this.#chunks.push(bytes)
  }

  toBytes() {
    const size = this.#chunks.reduce((total, chunk) => total + chunk.length, 0)
    const output = new Uint8Array(size)
    let offset = 0

    for (const chunk of this.#chunks) {
      output.set(chunk, offset)
      offset += chunk.length
    }

    return output
  }
}

class ByteReader {
  #offset = 0

  constructor(bytes) {
    this.bytes = bytes
  }

  readUint8() {
    if (this.#offset + 1 > this.bytes.length)
      throw new Error("Unexpected end of packed data")

    return this.bytes[this.#offset++] ?? 0
  }

  readUint32() {
    if (this.#offset + 4 > this.bytes.length)
      throw new Error("Unexpected end of packed data")

    const value = new DataView(
      this.bytes.buffer,
      this.bytes.byteOffset + this.#offset,
      4,
    ).getUint32(0, true)

    this.#offset += 4
    return value
  }

  readFloat64() {
    if (this.#offset + 8 > this.bytes.length)
      throw new Error("Unexpected end of packed data")

    const value = new DataView(
      this.bytes.buffer,
      this.bytes.byteOffset + this.#offset,
      8,
    ).getFloat64(0, true)

    this.#offset += 8
    return value
  }

  readBytes(length) {
    if (this.#offset + length > this.bytes.length)
      throw new Error("Unexpected end of packed data")

    const value = this.bytes.slice(this.#offset, this.#offset + length)
    this.#offset += length
    return value
  }
}

function encodeBigInt(value) {
  const absolute = value < 0n ? -value : value
  const hex = absolute.toString(16)
  const evenHex = hex.length % 2 === 0 ? hex : `0${hex}`
  return evenHex === "00" ? new Uint8Array([0]) : hexToBytes(evenHex)
}

function decodeBigInt(negative, bytes) {
  const absolute = bytes.length === 0 ? 0n : BigInt(`0x${bytesToHex(bytes)}`)
  return negative ? -absolute : absolute
}

function writeValue(writer, value) {
  if (value == null) {
    writer.writeUint8(0)
    return
  }

  if (typeof value === "number") {
    writer.writeUint8(1)
    writer.writeFloat64(value)
    return
  }

  if (value instanceof Uint8Array) {
    writer.writeUint8(2)
    writer.writeUint32(value.length)
    writer.writeBytes(value)
    return
  }

  if (typeof value === "string") {
    const data = new TextEncoder().encode(value)
    writer.writeUint8(3)
    writer.writeUint32(data.length)
    writer.writeBytes(data)
    return
  }

  if (typeof value === "bigint") {
    const encoded = encodeBigInt(value)
    writer.writeUint8(4)
    writer.writeUint8(value < 0n ? 1 : 0)
    writer.writeUint32(encoded.length)
    writer.writeBytes(encoded)
    return
  }

  if (Array.isArray(value)) {
    writer.writeUint8(5)
    writer.writeUint32(value.length)

    for (const item of value) writeValue(writer, item)

    return
  }

  throw new Error("Unknown pack value")
}

function readValue(reader) {
  const type = reader.readUint8()

  if (type === 0) return null
  if (type === 1) return reader.readFloat64()
  if (type === 2) return reader.readBytes(reader.readUint32())
  if (type === 3)
    return new TextDecoder().decode(reader.readBytes(reader.readUint32()))
  if (type === 4)
    return decodeBigInt(
      reader.readUint8(),
      reader.readBytes(reader.readUint32()),
    )
  if (type === 5) {
    const length = reader.readUint32()
    const values = []

    for (let i = 0; i < length; i++) values.push(readValue(reader))

    return values
  }

  throw new Error(`Unknown pack type: ${type}`)
}

export function pack(value) {
  const writer = new ByteWriter()
  writeValue(writer, value)
  return writer.toBytes()
}

export function unpack(bytes) {
  return readValue(new ByteReader(bytes))
}

export function jsonify(value) {
  if (value == null) return { type: "null" }
  if (typeof value === "number")
    return { type: "number", value: value.toString() }
  if (value instanceof Uint8Array)
    return { type: "blob", value: bytesToHex(value) }
  if (typeof value === "string") return { type: "text", value }
  if (typeof value === "bigint")
    return { type: "bigint", value: value.toString() }
  if (Array.isArray(value)) return { type: "array", value: value.map(jsonify) }

  throw new Error("Unknown pack value")
}
