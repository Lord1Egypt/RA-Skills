// ============================================================================
// Serial Port Service for Vibration Control System
// 串口通信服务 - 振动台控制系统
// ============================================================================
// Usage: Inject this service into your ViewModel or Controller
// Features:
//   - Async communication
//   - Thread-safe data buffering
//   - Event-driven data reception
//   - Automatic reconnection support
// ============================================================================

using System;
using System.Collections.Concurrent;
using System.IO.Ports;
using System.Threading;
using System.Threading.Tasks;

namespace VibrationControl.Services
{
    /// <summary>
    /// Provides serial port communication for actuator control.
    /// </summary>
    public class SerialPortService : IDisposable
    {
        private SerialPort? _serialPort;
        private readonly ConcurrentQueue<byte[]> _receiveBuffer;
        private readonly CancellationTokenSource _cancellationTokenSource;
        private bool _isConnected;
        private int _reconnectAttempts;
        
        private const int MaxReconnectAttempts = 3;
        private const int ReconnectDelayMs = 1000;
        private const int MaxBufferSize = 1000;

        /// <summary>
        /// Event raised when data is received.
        /// </summary>
        public event EventHandler<byte[]>? DataReceived;
        
        /// <summary>
        /// Event raised when connection status changes.
        /// </summary>
        public event EventHandler<bool>? ConnectionStatusChanged;

        /// <summary>
        /// Gets a value indicating whether the serial port is connected.
        /// </summary>
        public bool IsConnected => _isConnected && _serialPort?.IsOpen == true;

        /// <summary>
        /// Gets the number of bytes in the receive buffer.
        /// </summary>
        public int BufferCount => _receiveBuffer.Count;

        public SerialPortService()
        {
            _receiveBuffer = new ConcurrentQueue<byte[]>();
            _cancellationTokenSource = new CancellationTokenSource();
            _reconnectAttempts = 0;
        }

        /// <summary>
        /// Connects to the specified serial port.
        /// </summary>
        /// <param name="portName">COM port name (e.g., "COM3")</param>
        /// <param name="baudRate">Baud rate (default: 9600)</param>
        /// <param name="timeout">Connection timeout in seconds</param>
        public async Task ConnectAsync(string portName, int baudRate = 9600, int timeout = 10)
        {
            if (_isConnected)
            {
                throw new InvalidOperationException("Already connected");
            }

            try
            {
                _serialPort = new SerialPort(portName, baudRate)
                {
                    ReadTimeout = timeout * 1000,
                    WriteTimeout = timeout * 1000,
                    Parity = Parity.None,
                    StopBits = StopBits.One,
                    Handshake = Handshake.None,
                    RtsEnable = true,
                    DtrEnable = true
                };

                _serialPort.DataReceived += OnDataReceived;
                
                await Task.Run(() => _serialPort!.Open());
                
                _isConnected = true;
                _reconnectAttempts = 0;
                
                ConnectionStatusChanged?.Invoke(this, true);
                
                // Start background read loop
                _ = ReadLoopAsync(_cancellationTokenSource.Token);
            }
            catch (Exception ex)
            {
                throw new SerialPortException($"Failed to connect to {portName}: {ex.Message}", ex);
            }
        }

        /// <summary>
        /// Sends data asynchronously.
        /// </summary>
        /// <param name="data">Data to send</param>
        /// <param name="cancellationToken">Cancellation token</param>
        public async Task SendAsync(byte[] data, CancellationToken cancellationToken = default)
        {
            if (!IsConnected)
            {
                throw new InvalidOperationException("Not connected");
            }

            if (data == null || data.Length == 0)
            {
                throw new ArgumentException("Data cannot be empty", nameof(data));
            }

            try
            {
                await _serialPort!.BaseStream.WriteAsync(data, 0, data.Length, cancellationToken);
                await _serialPort.BaseStream.FlushAsync(cancellationToken);
            }
            catch (OperationCanceledException)
            {
                throw;
            }
            catch (Exception ex)
            {
                throw new SerialPortException($"Failed to send data: {ex.Message}", ex);
            }
        }

        /// <summary>
        /// Sends a command and waits for response.
        /// </summary>
        /// <param name="command">Command bytes</param>
        /// <param name="timeoutMs">Response timeout in milliseconds</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Response bytes</returns>
        public async Task<byte[]> SendCommandAsync(
            byte[] command, 
            int timeoutMs = 5000, 
            CancellationToken cancellationToken = default)
        {
            await SendAsync(command, cancellationToken);
            
            var stopwatch = System.Diagnostics.Stopwatch.StartNew();
            
            while (stopwatch.ElapsedMilliseconds < timeoutMs)
            {
                if (_receiveBuffer.TryDequeue(out var response))
                {
                    return response;
                }
                
                await Task.Delay(10, cancellationToken);
            }
            
            throw new TimeoutException("No response received within timeout period");
        }

        /// <summary>
        /// Gets recent data from the receive buffer.
        /// </summary>
        /// <param name="count">Number of items to retrieve</param>
        /// <returns>Recent data items</returns>
        public byte[][] GetRecentData(int count)
        {
            var result = new System.Collections.Generic.List<byte[]>(count);
            
            while (result.Count < count && _receiveBuffer.TryDequeue(out var data))
            {
                result.Add(data);
            }
            
            return result.ToArray();
        }

        /// <summary>
        /// Clears the receive buffer.
        /// </summary>
        public void ClearBuffer()
        {
            while (_receiveBuffer.TryDequeue(out _)) { }
        }

        /// <summary>
        /// Disconnects from the serial port.
        /// </summary>
        public async Task DisconnectAsync()
        {
            if (!_isConnected)
            {
                return;
            }

            try
            {
                _cancellationTokenSource.Cancel();
                
                if (_serialPort != null)
                {
                    _serialPort.DataReceived -= OnDataReceived;
                    
                    if (_serialPort.IsOpen)
                    {
                        _serialPort.Close();
                    }
                    
                    _serialPort.Dispose();
                    _serialPort = null;
                }
                
                _isConnected = false;
                ConnectionStatusChanged?.Invoke(this, false);
            }
            catch (Exception ex)
            {
                throw new SerialPortException($"Failed to disconnect: {ex.Message}", ex);
            }
        }

        /// <summary>
        /// Background read loop for continuous data reception.
        /// </summary>
        private async Task ReadLoopAsync(CancellationToken cancellationToken)
        {
            var buffer = new byte[1024];
            
            try
            {
                while (!cancellationToken.IsCancellationRequested && IsConnected)
                {
                    try
                    {
                        int bytesRead = await _serialPort!.BaseStream.ReadAsync(
                            buffer, 0, buffer.Length, cancellationToken);
                        
                        if (bytesRead > 0)
                        {
                            var data = new byte[bytesRead];
                            Buffer.BlockCopy(buffer, 0, data, 0, bytesRead);
                            
                            _receiveBuffer.Enqueue(data);
                            
                            // Enforce buffer size limit
                            while (_receiveBuffer.Count > MaxBufferSize)
                            {
                                _receiveBuffer.TryDequeue(out _);
                            }
                            
                            DataReceived?.Invoke(this, data);
                        }
                    }
                    catch (TimeoutException)
                    {
                        // Expected when no data available
                        await Task.Delay(10, cancellationToken);
                    }
                    catch (OperationCanceledException)
                    {
                        break;
                    }
                    catch (IOException)
                    {
                        // Connection lost, attempt reconnection
                        await HandleReconnectionAsync();
                    }
                }
            }
            catch (OperationCanceledException)
            {
                // Expected on cancellation
            }
            catch (Exception ex)
            {
                // Log error but don't crash the read loop
                System.Diagnostics.Debug.WriteLine($"ReadLoop error: {ex}");
            }
        }

        /// <summary>
        /// Handles automatic reconnection on connection loss.
        /// </summary>
        private async Task HandleReconnectionAsync()
        {
            if (_reconnectAttempts >= MaxReconnectAttempts)
            {
                await DisconnectAsync();
                return;
            }

            _reconnectAttempts++;
            
            try
            {
                await Task.Delay(ReconnectDelayMs * _reconnectAttempts);
                
                if (_serialPort != null && !_isConnected)
                {
                    _serialPort.Close();
                    _serialPort.Open();
                    _isConnected = true;
                    _reconnectAttempts = 0;
                    ConnectionStatusChanged?.Invoke(this, true);
                }
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Reconnection failed (attempt {_reconnectAttempts}): {ex}");
            }
        }

        /// <summary>
        /// Event handler for serial port data received event.
        /// </summary>
        private void OnDataReceived(object sender, SerialDataReceivedEventArgs e)
        {
            // Data is handled in ReadLoopAsync
        }

        /// <summary>
        /// Disposes of the serial port resources.
        /// </summary>
        public void Dispose()
        {
            _cancellationTokenSource.Cancel();
            _cancellationTokenSource.Dispose();
            DisconnectAsync().Wait();
        }
    }

    /// <summary>
    /// Exception thrown for serial port errors.
    /// </summary>
    public class SerialPortException : Exception
    {
        public SerialPortException(string message) : base(message) { }
        public SerialPortException(string message, Exception innerException) 
            : base(message, innerException) { }
    }
}
