import React, { useState, useRef } from 'react';

export default function AudioPTInterface() {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [selectedVoice, setSelectedVoice] = useState('jeff');
  const [transcript, setTranscript] = useState('');
  const [response, setResponse] = useState('');
  const [audioFile, setAudioFile] = useState(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const voices = [
    { id: 'jeff', name: 'Jeff', gender: 'Masculino', quality: 'Médio' },
    { id: 'cadu', name: 'Cadu', gender: 'Masculino', quality: 'Médio' },
    { id: 'faber', name: 'Faber', gender: 'Masculino', quality: 'Médio' },
    { id: 'miro', name: 'Miro', gender: 'Feminino', quality: 'Alto' },
  ];

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        setAudioFile(audioBlob);
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      alert('Erro ao acessar microfone: ' + error.message);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const processAudio = async () => {
    if (!audioFile) return;

    setIsProcessing(true);
    setTranscript('');
    setResponse('');

    try {
      // Simular processamento
      // Em produção, isso chamaria a API real
      
      setTranscript('Exemplo: "Qual é a capital da França?"');
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setResponse('A capital da França é Paris.');
      
    } catch (error) {
      setResponse('Erro ao processar áudio');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleFileUpload = (event) => {
    const file = event.target.files?.[0];
    if (file) {
      setAudioFile(file);
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '1rem' }}>
      {/* Header */}
      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '22px', fontWeight: 500, margin: '0 0 0.5rem', color: 'var(--color-text-primary)' }}>
          🎙️ Audio PT Auto-Reply
        </h1>
        <p style={{ fontSize: '14px', color: 'var(--color-text-secondary)', margin: 0 }}>
          Transcrição e respostas em áudio português brasileiro
        </p>
      </div>

      {/* Voice Selection */}
      <div style={{ marginBottom: '1.5rem' }}>
        <label style={{ fontSize: '14px', fontWeight: 500, color: 'var(--color-text-primary)', display: 'block', marginBottom: '0.75rem' }}>
          Selecione uma voz:
        </label>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '12px' }}>
          {voices.map((voice) => (
            <button
              key={voice.id}
              onClick={() => setSelectedVoice(voice.id)}
              style={{
                padding: '12px',
                border: selectedVoice === voice.id ? '2px solid var(--color-border-info)' : '0.5px solid var(--color-border-tertiary)',
                borderRadius: 'var(--border-radius-md)',
                background: selectedVoice === voice.id ? 'var(--color-background-secondary)' : 'var(--color-background-primary)',
                cursor: 'pointer',
                textAlign: 'left',
                transition: 'all 0.2s',
              }}
            >
              <div style={{ fontSize: '14px', fontWeight: 500, color: 'var(--color-text-primary)' }}>
                {voice.name}
              </div>
              <div style={{ fontSize: '12px', color: 'var(--color-text-secondary)' }}>
                {voice.gender} • {voice.quality}
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Recording Controls */}
      <div style={{ marginBottom: '1.5rem', padding: '1rem', background: 'var(--color-background-secondary)', borderRadius: 'var(--border-radius-lg)', border: '0.5px solid var(--color-border-tertiary)' }}>
        <p style={{ fontSize: '14px', fontWeight: 500, color: 'var(--color-text-primary)', margin: '0 0 12px' }}>
          Gravação de áudio:
        </p>
        
        <div style={{ display: 'flex', gap: '12px', marginBottom: '12px' }}>
          {!isRecording ? (
            <button
              onClick={startRecording}
              style={{
                flex: 1,
                padding: '12px',
                background: 'transparent',
                border: '0.5px solid var(--color-border-secondary)',
                borderRadius: 'var(--border-radius-md)',
                cursor: 'pointer',
                fontSize: '14px',
                fontWeight: 500,
                color: 'var(--color-text-primary)',
              }}
            >
              🎤 Iniciar gravação
            </button>
          ) : (
            <button
              onClick={stopRecording}
              style={{
                flex: 1,
                padding: '12px',
                background: 'var(--color-background-danger)',
                border: 'none',
                borderRadius: 'var(--border-radius-md)',
                cursor: 'pointer',
                fontSize: '14px',
                fontWeight: 500,
                color: 'white',
              }}
            >
              ⏹️ Parar gravação
            </button>
          )}
        </div>

        <div style={{ fontSize: '13px', color: 'var(--color-text-secondary)' }}>
          ou
        </div>

        <div style={{ marginTop: '12px' }}>
          <input
            type="file"
            accept="audio/*"
            onChange={handleFileUpload}
            style={{ fontSize: '13px' }}
          />
          {audioFile && (
            <div style={{ fontSize: '12px', color: 'var(--color-text-secondary)', marginTop: '8px' }}>
              ✓ Arquivo selecionado
            </div>
          )}
        </div>
      </div>

      {/* Process Button */}
      {audioFile && (
        <button
          onClick={processAudio}
          disabled={isProcessing}
          style={{
            width: '100%',
            padding: '12px',
            background: 'transparent',
            border: '0.5px solid var(--color-border-secondary)',
            borderRadius: 'var(--border-radius-md)',
            cursor: isProcessing ? 'not-allowed' : 'pointer',
            fontSize: '14px',
            fontWeight: 500,
            color: 'var(--color-text-primary)',
            opacity: isProcessing ? 0.6 : 1,
            marginBottom: '1.5rem',
          }}
        >
          {isProcessing ? '⏳ Processando...' : '🚀 Processar áudio'}
        </button>
      )}

      {/* Results */}
      {(transcript || response) && (
        <>
          {transcript && (
            <div style={{ marginBottom: '1.5rem', padding: '1rem', background: 'var(--color-background-secondary)', borderRadius: 'var(--border-radius-lg)', border: '0.5px solid var(--color-border-tertiary)' }}>
              <p style={{ fontSize: '12px', fontWeight: 500, color: 'var(--color-text-secondary)', margin: '0 0 8px', textTransform: 'uppercase' }}>
                Transcrição
              </p>
              <p style={{ fontSize: '14px', color: 'var(--color-text-primary)', margin: 0 }}>
                {transcript}
              </p>
            </div>
          )}

          {response && (
            <div style={{ padding: '1rem', background: 'var(--color-background-secondary)', borderRadius: 'var(--border-radius-lg)', border: '0.5px solid var(--color-border-tertiary)' }}>
              <p style={{ fontSize: '12px', fontWeight: 500, color: 'var(--color-text-secondary)', margin: '0 0 8px', textTransform: 'uppercase' }}>
                Resposta
              </p>
              <p style={{ fontSize: '14px', color: 'var(--color-text-primary)', margin: 0 }}>
                {response}
              </p>
            </div>
          )}
        </>
      )}

      {/* Info */}
      <div style={{ marginTop: '2rem', padding: '1rem', background: 'var(--color-background-secondary)', borderRadius: 'var(--border-radius-md)', border: '0.5px solid var(--color-border-tertiary)' }}>
        <p style={{ fontSize: '12px', color: 'var(--color-text-secondary)', margin: 0 }}>
          💡 <strong>Dica:</strong> Fale naturalmente em português brasileiro. O sistema entende slang, sotaques e expressões coloquiais.
        </p>
      </div>
    </div>
  );
}
